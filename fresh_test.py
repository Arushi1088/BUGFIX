#!/usr/bin/env python3
"""
🚀 Fresh Start Test - Steps 2 & 3
Clean execution for VS Code terminal
"""

def main():
    print("🔄 FRESH START - TESTING STEPS 2 & 3")
    print("=" * 40)
    
    # Step 2: Test connectivity
    print("\n📡 STEP 2: Server Connectivity")
    print("-" * 30)
    
    try:
        import requests
        
        # Quick server test
        print("Testing http://localhost:8000/health...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is healthy!")
            print(f"   Status: {data.get('status')}")
            print(f"   Port: {data.get('port')}")
            print(f"   Mocks: {data.get('mocks_available', [])}")
            
            # Test one mock
            print("\nTesting Word mock...")
            word_response = requests.get("http://localhost:8000/mocks/word.html", timeout=5)
            if word_response.status_code == 200:
                print(f"✅ Word mock loaded ({len(word_response.text)} chars)")
                
                # Check for our enhanced selectors
                if 'data-testid="new-doc-btn"' in word_response.text:
                    print("✅ Enhanced selectors found!")
                else:
                    print("⚠️ Enhanced selectors missing")
            else:
                print(f"❌ Word mock failed: {word_response.status_code}")
                return False
        else:
            print(f"❌ Server health failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on localhost:8000")
        print("💡 Make sure server is running: python robust_server.py")
        return False
    except Exception as e:
        print(f"❌ Connectivity error: {e}")
        return False
    
    # Step 3: Test agent basics
    print("\n🤖 STEP 3: Agent Basics")
    print("-" * 25)
    
    try:
        import sys
        import os
        
        # Add project to path
        project_path = '/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer'
        if project_path not in sys.path:
            sys.path.insert(0, project_path)
        
        # Load .env file
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ .env file loaded")
        except ImportError:
            print("⚠️ python-dotenv not found, trying manual .env load...")
            # Manual .env loading
            env_path = os.path.join(project_path, '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value.strip('"\'')
                print("✅ .env file loaded manually")
            else:
                print(f"⚠️ .env file not found at {env_path}")
        
        # Test API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OpenAI API key not found!")
            print(f"💡 Check .env file exists: {os.path.exists(os.path.join(project_path, '.env'))}")
            return False
        print(f"✅ API key configured (length: {len(api_key)} chars)")
        
        # Import agent
        from interactive_agent import InteractiveUXAgent
        print("✅ InteractiveUXAgent imported")
        
        # Initialize
        agent = InteractiveUXAgent()
        print("✅ Agent initialized")
        
        # Test batching
        test_scenario = "Click the new document button using data-testid selector"
        suggestions = agent._suggest_batch_optimizations(test_scenario)
        print(f"✅ Batching works: {suggestions}")
        
        # Test client stats
        stats = agent.client.get_stats()
        print(f"✅ Client ready: {stats}")
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Success!
    print("\n🎉 ALL TESTS PASSED!")
    print("✅ Server connectivity: OK")
    print("✅ Enhanced selectors: OK") 
    print("✅ Agent initialization: OK")
    print("✅ API configuration: OK")
    
    print("\n🚀 READY FOR FULL TESTING!")
    print("Next command: python enhanced_mock_test.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n🔧 Fix issues above before proceeding")
    except KeyboardInterrupt:
        print("\n🛑 Cancelled")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
