#!/usr/bin/env python3
"""
🔄 OpenAI Client Wrapper with Rate Limiting & Retry Logic
Handles 429 errors gracefully with exponential backoff and model fallback.
"""

import json
import time
import random
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import openai
from openai import OpenAI


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_retries: int = 3
    base_delay: float = 1.0  # Initial delay in seconds
    max_delay: float = 60.0  # Maximum delay in seconds
    exponential_base: float = 2.0  # Exponential backoff multiplier
    jitter: bool = True  # Add random jitter to prevent thundering herd


class RateLimitError(Exception):
    """Custom exception for rate limit handling."""
    def __init__(self, message: str, retry_after: Optional[float] = None):
        super().__init__(message)
        self.retry_after = retry_after


class _ChatInterface:
    """OpenAI-compatible chat interface for the wrapper."""
    
    def __init__(self, wrapper):
        self.wrapper = wrapper
    
    @property
    def completions(self):
        """Provide completions interface."""
        return _CompletionsInterface(self.wrapper)


class _CompletionsInterface:
    """OpenAI-compatible completions interface."""
    
    def __init__(self, wrapper):
        self.wrapper = wrapper
    
    def create(self, **kwargs):
        """Create a chat completion using the wrapper's method."""
        return self.wrapper.chat_completion(**kwargs)


class OpenAIClientWrapper:
    """
    Wrapper around OpenAI client with robust rate limiting and retry logic.
    
    Features:
    - Exponential backoff on 429 errors
    - Model fallback (GPT-4o → GPT-3.5-turbo)
    - Automatic retry with jitter
    - Request/response logging
    """
    
    def __init__(self, 
                 primary_model: str = "gpt-4o",
                 fallback_model: str = "gpt-3.5-turbo",
                 retry_config: Optional[RetryConfig] = None,
                 client: Optional[OpenAI] = None):
        self.client = client or OpenAI()
        self.primary_model = primary_model
        self.fallback_model = fallback_model
        self.retry_config = retry_config or RetryConfig()
        
        # Statistics tracking
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'rate_limited_requests': 0,
            'fallback_requests': 0,
            'failed_requests': 0
        }
    
    @property
    def chat(self):
        """Provide OpenAI-compatible chat interface."""
        return _ChatInterface(self)
    
    def chat_completion(self,
                       messages: List[Dict[str, Any]],
                       model: Optional[str] = None,
                       tools: Optional[List[Dict[str, Any]]] = None,
                       tool_choice: Optional[Union[str, Dict]] = None,
                       temperature: float = 0.1,
                       max_tokens: Optional[int] = None,
                       enable_fallback: bool = True,
                       **kwargs) -> Any:
        """
        Create a chat completion with rate limiting and retry logic.
        
        Args:
            messages: Conversation messages
            model: Model to use (defaults to primary_model)
            tools: Function tools for function calling
            tool_choice: Tool choice strategy
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            enable_fallback: Whether to fall back to secondary model on rate limits
            **kwargs: Additional OpenAI API parameters
            
        Returns:
            OpenAI ChatCompletion response
            
        Raises:
            RateLimitError: If all retries exhausted
            Exception: For other API errors
        """
        model = model or self.primary_model
        self.stats['total_requests'] += 1
        
        # Prepare request parameters
        request_params = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            **kwargs
        }
        
        if tools is not None:
            request_params['tools'] = tools
        if tool_choice is not None:
            request_params['tool_choice'] = tool_choice
        if max_tokens is not None:
            request_params['max_tokens'] = max_tokens
        
        # Retry loop with exponential backoff
        last_exception = None
        
        for attempt in range(self.retry_config.max_retries + 1):
            try:
                print(f"🔄 OpenAI request (attempt {attempt + 1}/{self.retry_config.max_retries + 1}): {model}")
                
                # Make the API call
                response = self.client.chat.completions.create(**request_params)
                
                self.stats['successful_requests'] += 1
                print(f"✅ OpenAI request successful")
                return response
                
            except openai.RateLimitError as e:
                self.stats['rate_limited_requests'] += 1
                last_exception = e
                
                # Extract retry_after from error if available
                retry_after = self._extract_retry_after(e)
                
                print(f"⏳ Rate limit hit (attempt {attempt + 1}): {e}")
                
                # If this is the last attempt, try fallback model if enabled
                if attempt == self.retry_config.max_retries:
                    if enable_fallback and model != self.fallback_model:
                        print(f"🔄 Falling back to {self.fallback_model}")
                        request_params['model'] = self.fallback_model
                        self.stats['fallback_requests'] += 1
                        
                        try:
                            response = self.client.chat.completions.create(**request_params)
                            self.stats['successful_requests'] += 1
                            print(f"✅ Fallback request successful")
                            return response
                        except Exception as fallback_error:
                            print(f"❌ Fallback also failed: {fallback_error}")
                            raise RateLimitError(f"Both primary and fallback models rate limited: {e}")
                    else:
                        raise RateLimitError(f"Rate limit exhausted after {self.retry_config.max_retries} retries: {e}", retry_after)
                
                # Calculate delay for next attempt
                delay = self._calculate_delay(attempt, retry_after)
                print(f"⏰ Waiting {delay:.2f}s before retry...")
                time.sleep(delay)
                
            except Exception as e:
                self.stats['failed_requests'] += 1
                print(f"❌ OpenAI request failed: {e}")
                raise e
        
        # Should never reach here, but just in case
        self.stats['failed_requests'] += 1
        raise RateLimitError(f"Unexpected failure after retries: {last_exception}")
    
    def _extract_retry_after(self, error: openai.RateLimitError) -> Optional[float]:
        """Extract retry_after value from rate limit error."""
        try:
            # Try to parse the error message for retry_after information
            error_str = str(error)
            if "try again in" in error_str.lower():
                # Look for patterns like "try again in 2.482s"
                import re
                match = re.search(r'try again in ([\d.]+)s', error_str)
                if match:
                    return float(match.group(1))
        except:
            pass
        return None
    
    def _calculate_delay(self, attempt: int, retry_after: Optional[float] = None) -> float:
        """Calculate delay before next retry attempt."""
        if retry_after:
            # Use server-provided retry_after if available
            delay = retry_after
        else:
            # Exponential backoff: base_delay * (exponential_base ^ attempt)
            delay = self.retry_config.base_delay * (self.retry_config.exponential_base ** attempt)
        
        # Cap at max_delay
        delay = min(delay, self.retry_config.max_delay)
        
        # Add jitter to prevent thundering herd
        if self.retry_config.jitter:
            jitter_amount = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_amount, jitter_amount)
        
        return max(0, delay)  # Ensure non-negative
    
    def get_stats(self) -> Dict[str, Any]:
        """Get client usage statistics."""
        total = self.stats['total_requests']
        if total == 0:
            return self.stats.copy()
        
        stats_with_percentages = self.stats.copy()
        stats_with_percentages.update({
            'success_rate': (self.stats['successful_requests'] / total) * 100,
            'rate_limit_rate': (self.stats['rate_limited_requests'] / total) * 100,
            'fallback_rate': (self.stats['fallback_requests'] / total) * 100,
            'failure_rate': (self.stats['failed_requests'] / total) * 100
        })
        return stats_with_percentages
    
    def reset_stats(self):
        """Reset usage statistics."""
        for key in self.stats:
            self.stats[key] = 0


# Convenience function for backwards compatibility
def create_chat_completion(*args, **kwargs):
    """Create a chat completion using the default wrapper instance."""
    if not hasattr(create_chat_completion, '_client'):
        create_chat_completion._client = OpenAIClientWrapper()
    return create_chat_completion._client.chat_completion(*args, **kwargs)


if __name__ == "__main__":
    # Quick test of the wrapper
    print("🧪 Testing OpenAI Client Wrapper...")
    
    client = OpenAIClientWrapper()
    
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in exactly 3 words."}
            ],
            max_tokens=10
        )
        
        print(f"✅ Test successful: {response.choices[0].message.content}")
        print(f"📊 Stats: {client.get_stats()}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
