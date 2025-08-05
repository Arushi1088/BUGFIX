#!/usr/bin/env python3
"""
🧪 Tests for OpenAI Client Wrapper Rate Limiting
Tests the rate limit handling, retry logic, and fallback behavior.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import time
import openai
from openai_client import OpenAIClientWrapper, RateLimitError, RetryConfig


class TestOpenAIClientWrapper(unittest.TestCase):
    """Test cases for OpenAI client wrapper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.retry_config = RetryConfig(
            max_retries=2,
            base_delay=0.1,  # Fast for testing
            max_delay=1.0,
            exponential_base=2.0,
            jitter=False  # Deterministic for testing
        )
        # Create a mock client to avoid API key issues
        self.mock_client = Mock()
        self.client = OpenAIClientWrapper(
            primary_model="gpt-4o",
            fallback_model="gpt-3.5-turbo",
            retry_config=self.retry_config,
            client=self.mock_client
        )
    
    def test_successful_request(self):
        """Test a successful request without rate limiting."""
        # Mock successful response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Hello world!"
        
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # Test request
        response = self.client.chat_completion(
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        # Verify
        self.assertIsNotNone(response)
        self.assertEqual(response.choices[0].message.content, "Hello world!")
        
        stats = self.client.get_stats()
        self.assertEqual(stats['total_requests'], 1)
        self.assertEqual(stats['successful_requests'], 1)
        self.assertEqual(stats['rate_limited_requests'], 0)
    
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_rate_limit_retry_success(self, mock_sleep):
        """Test rate limit handling with eventual success."""
        # Mock rate limit error first, then success
        rate_limit_error = openai.RateLimitError("Rate limit exceeded")
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Success after retry"
        
        self.mock_client.chat.completions.create.side_effect = [
            rate_limit_error,  # First call fails
            mock_response      # Second call succeeds
        ]
        
        # Test request
        response = self.client.chat_completion(
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        # Verify
        self.assertIsNotNone(response)
        self.assertEqual(response.choices[0].message.content, "Success after retry")
        
        # Verify sleep was called for backoff
        mock_sleep.assert_called_once()
        
        stats = self.client.get_stats()
        self.assertEqual(stats['total_requests'], 1)
        self.assertEqual(stats['successful_requests'], 1)
        self.assertEqual(stats['rate_limited_requests'], 1)
    
    @patch('openai_client.OpenAI')
    @patch('time.sleep')
    def test_rate_limit_fallback_success(self, mock_sleep, mock_openai):
        """Test fallback to secondary model on persistent rate limits."""
        # Mock rate limit errors for primary model
        rate_limit_error = openai.RateLimitError("Rate limit exceeded")
        
        # Mock successful response from fallback
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Fallback success"
        
        mock_client = Mock()
        # Primary model fails all retries, fallback succeeds
        mock_client.chat.completions.create.side_effect = [
            rate_limit_error,  # Attempt 1: primary fails
            rate_limit_error,  # Attempt 2: primary fails
            rate_limit_error,  # Attempt 3: primary fails
            mock_response      # Fallback succeeds
        ]
        mock_openai.return_value = mock_client
        
        # Create new client with mocked OpenAI
        client = OpenAIClientWrapper(retry_config=self.retry_config)
        
        # Test request
        response = client.chat_completion(
            messages=[{"role": "user", "content": "Hello"}],
            enable_fallback=True
        )
        
        # Verify
        self.assertIsNotNone(response)
        self.assertEqual(response.choices[0].message.content, "Fallback success")
        
        stats = client.get_stats()
        self.assertEqual(stats['total_requests'], 1)
        self.assertEqual(stats['successful_requests'], 1)
        self.assertEqual(stats['fallback_requests'], 1)
        self.assertEqual(stats['rate_limited_requests'], 1)
    
    @patch('openai_client.OpenAI')
    @patch('time.sleep')
    def test_rate_limit_exhaustion(self, mock_sleep, mock_openai):
        """Test behavior when all retries are exhausted."""
        # Mock persistent rate limit errors
        rate_limit_error = openai.RateLimitError("Rate limit exceeded")
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = rate_limit_error
        mock_openai.return_value = mock_client
        
        # Create new client with mocked OpenAI
        client = OpenAIClientWrapper(retry_config=self.retry_config)
        
        # Test request should raise RateLimitError
        with self.assertRaises(RateLimitError):
            client.chat_completion(
                messages=[{"role": "user", "content": "Hello"}],
                enable_fallback=False  # Disable fallback to test exhaustion
            )
        
        stats = client.get_stats()
        self.assertEqual(stats['total_requests'], 1)
        self.assertEqual(stats['successful_requests'], 0)
        self.assertEqual(stats['failed_requests'], 1)
    
    def test_retry_after_extraction(self):
        """Test extraction of retry_after value from error messages."""
        client = OpenAIClientWrapper()
        
        # Test with retry_after in message
        error_with_retry = openai.RateLimitError(
            "Rate limit reached. Please try again in 2.482s."
        )
        retry_after = client._extract_retry_after(error_with_retry)
        self.assertAlmostEqual(retry_after, 2.482, places=3)
        
        # Test without retry_after
        error_without_retry = openai.RateLimitError("Rate limit reached")
        retry_after = client._extract_retry_after(error_without_retry)
        self.assertIsNone(retry_after)
    
    def test_delay_calculation(self):
        """Test exponential backoff delay calculation."""
        client = OpenAIClientWrapper(retry_config=self.retry_config)
        
        # Test exponential backoff
        delay0 = client._calculate_delay(0)
        delay1 = client._calculate_delay(1)
        delay2 = client._calculate_delay(2)
        
        # Should follow exponential pattern: base * (exponential_base ^ attempt)
        expected0 = 0.1  # base_delay
        expected1 = 0.1 * 2  # base_delay * exponential_base^1
        expected2 = 0.1 * 4  # base_delay * exponential_base^2
        
        self.assertAlmostEqual(delay0, expected0, places=2)
        self.assertAlmostEqual(delay1, expected1, places=2)
        self.assertAlmostEqual(delay2, expected2, places=2)
        
        # Test with retry_after override
        delay_with_retry = client._calculate_delay(0, retry_after=5.0)
        self.assertEqual(delay_with_retry, 5.0)
        
        # Test max_delay cap
        delay_capped = client._calculate_delay(10)  # Very high attempt
        self.assertLessEqual(delay_capped, self.retry_config.max_delay)
    
    def test_stats_tracking(self):
        """Test statistics tracking functionality."""
        client = OpenAIClientWrapper()
        
        # Initial stats should be zero
        stats = client.get_stats()
        for value in stats.values():
            if isinstance(value, int):
                self.assertEqual(value, 0)
        
        # Reset should work
        client.reset_stats()
        stats = client.get_stats()
        for value in stats.values():
            if isinstance(value, int):
                self.assertEqual(value, 0)


class TestRetryConfig(unittest.TestCase):
    """Test cases for RetryConfig dataclass."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = RetryConfig()
        
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.base_delay, 1.0)
        self.assertEqual(config.max_delay, 60.0)
        self.assertEqual(config.exponential_base, 2.0)
        self.assertTrue(config.jitter)
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = RetryConfig(
            max_retries=5,
            base_delay=0.5,
            max_delay=30.0,
            exponential_base=1.5,
            jitter=False
        )
        
        self.assertEqual(config.max_retries, 5)
        self.assertEqual(config.base_delay, 0.5)
        self.assertEqual(config.max_delay, 30.0)
        self.assertEqual(config.exponential_base, 1.5)
        self.assertFalse(config.jitter)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
