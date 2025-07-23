#!/usr/bin/env python3
"""
Debug Gemini API Calls - Show exact API key and endpoint being used
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Import CrewAI and LangChain components
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def setup_debug_logging():
    """Setup detailed logging to see API calls"""
    
    # Set up detailed logging for relevant modules
    logging.getLogger("langchain_google_genai").setLevel(logging.DEBUG)
    logging.getLogger("google.generativeai").setLevel(logging.DEBUG)
    logging.getLogger("crewai").setLevel(logging.DEBUG)
    
    # Create a detailed formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add console handler with detailed formatting
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Get the root logger and configure it
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

def debug_gemini_configuration():
    """Debug Gemini configuration with detailed API information"""
    
    print("🔍 GEMINI API CONFIGURATION DEBUG")
    print("=" * 60)
    
    # Check environment variable
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    print(f"📋 Environment Variable Check:")
    print(f"   GEMINI_API_KEY exists: {gemini_api_key is not None}")
    
    if gemini_api_key:
        print(f"   API Key length: {len(gemini_api_key)} characters")
        print(f"   API Key starts with: {gemini_api_key[:10]}...")
        print(f"   API Key ends with: ...{gemini_api_key[-10:]}")
        print(f"   Full API Key: {gemini_api_key}")  # Show full key for debugging
        
        # Check if it's the test key
        if gemini_api_key == "test-key":
            print("   ❌ This is the test placeholder key!")
            return None
        
        # Check if it has the right format
        if gemini_api_key.startswith("AIza"):
            print("   ✅ API Key has correct format (starts with AIza)")
        else:
            print("   ⚠️  API Key doesn't start with 'AIza' - might be invalid")
    else:
        print("   ❌ No API key found!")
        return None
    
    print()
    
    # Show Gemini endpoint information
    print("🌐 Gemini API Endpoint Information:")
    print("   Base URL: https://generativelanguage.googleapis.com")
    print("   Model endpoint: /v1beta/models/gemini-1.5-flash:generateContent")
    print("   Full URL: https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent")
    print("   Authentication: API Key in query parameter or header")
    print()
    
    # Create LLM with debug information
    print("🤖 Creating Gemini LLM with debug info...")
    
    try:
        # Create the LLM instance
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.1,
            convert_system_message_to_human=True,
            verbose=True,  # Enable verbose mode
        )
        
        print("✅ LLM created successfully!")
        
        # Show LLM configuration details
        print(f"📋 LLM Configuration:")
        print(f"   Model: {llm.model}")
        print(f"   Temperature: {llm.temperature}")
        print(f"   API Key (first 10 chars): {llm.google_api_key[:10]}...")
        print(f"   Max tokens: {getattr(llm, 'max_tokens', 'default')}")
        print(f"   Convert system message: {getattr(llm, 'convert_system_message_to_human', 'default')}")
        
        return llm
        
    except Exception as e:
        print(f"❌ LLM creation failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check for specific error types
        if "API_KEY" in str(e).upper():
            print("   💡 This appears to be an API key issue")
        elif "QUOTA" in str(e).upper():
            print("   💡 This appears to be a quota/billing issue")
        elif "NETWORK" in str(e).upper() or "CONNECTION" in str(e).upper():
            print("   💡 This appears to be a network connectivity issue")
        
        import traceback
        traceback.print_exc()
        
        return None

def test_direct_api_call(api_key):
    """Test direct API call to Gemini to see the exact request"""
    
    print("\n🧪 TESTING DIRECT GEMINI API CALL")
    print("-" * 40)
    
    try:
        import google.generativeai as genai
        
        # Configure the client
        genai.configure(api_key=api_key)
        
        print(f"📡 API Configuration:")
        print(f"   Client configured with key: {api_key[:10]}...{api_key[-10:]}")
        
        # Test a simple generation
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print(f"📤 Making test API call...")
        print(f"   Model: gemini-1.5-flash")
        print(f"   Prompt: 'Hello, please confirm you are working'")
        
        response = model.generate_content("Hello, please confirm you are working")
        
        print(f"📨 API Response:")
        print(f"   Status: ✅ Success")
        print(f"   Response text: {response.text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"📨 API Response:")
        print(f"   Status: ❌ Failed")
        print(f"   Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Show more detailed error info
        import traceback
        print(f"\n📋 Full error traceback:")
        traceback.print_exc()
        
        return False

def test_langchain_integration(llm):
    """Test LangChain integration with debug logging"""
    
    print("\n🔗 TESTING LANGCHAIN INTEGRATION")
    print("-" * 40)
    
    try:
        print("📤 Making LangChain API call...")
        print("   Method: llm.invoke()")
        print("   Message: 'Test message for debugging'")
        
        # Enable debug logging temporarily
        import logging
        logging.getLogger("langchain_google_genai").setLevel(logging.DEBUG)
        
        response = llm.invoke("Test message for debugging")
        
        print(f"📨 LangChain Response:")
        print(f"   Status: ✅ Success")
        print(f"   Response type: {type(response)}")
        print(f"   Response content: {response.content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"📨 LangChain Response:")
        print(f"   Status: ❌ Failed")
        print(f"   Error: {e}")
        
        import traceback
        traceback.print_exc()
        
        return False

def test_crewai_integration(llm):
    """Test CrewAI integration with detailed logging"""
    
    print("\n👥 TESTING CREWAI INTEGRATION")
    print("-" * 40)
    
    try:
        # Create a simple agent
        agent = Agent(
            role='Debug Agent',
            goal='Test API connectivity',
            backstory='Testing agent for API debugging',
            llm=llm,
            verbose=True
        )
        
        print("✅ Agent created successfully")
        
        # Create a simple task
        task = Task(
            description="Say hello and confirm the API is working",
            expected_output="A simple hello message",
            agent=agent
        )
        
        print("✅ Task created successfully")
        
        # Create crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        print("✅ Crew created successfully")
        
        print("📤 Starting crew execution...")
        print("   This will show the actual API calls CrewAI makes")
        
        result = crew.kickoff()
        
        print(f"📨 CrewAI Execution:")
        print(f"   Status: ✅ Success")
        print(f"   Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"📨 CrewAI Execution:")
        print(f"   Status: ❌ Failed")  
        print(f"   Error: {e}")
        
        # Check if this is our "unknown error occurred"
        if "unknown error occurred" in str(e).lower():
            print("   🎯 This is the 'unknown error occurred' we're debugging!")
        
        import traceback
        traceback.print_exc()
        
        return False

class DebugMCPTool(BaseTool):
    """Simple debug tool for testing"""
    name: str = "debug_tool"
    description: str = "A simple debug tool for testing"
    
    def _run(self, query: str = "test") -> str:
        print(f"🔧 Tool called with query: {query}")
        return f"Tool executed successfully with query: {query}"

def main():
    """Main debug function"""
    
    print("🐛 GEMINI API DEBUG SESSION")
    print("=" * 60)
    print(f"🕐 Debug time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Goal: Debug exact API calls and configuration")
    print("=" * 60)
    
    # Setup debug logging
    setup_debug_logging()
    
    # Step 1: Debug configuration
    llm = debug_gemini_configuration()
    if not llm:
        print("\n❌ Cannot proceed - LLM configuration failed")
        return False
    
    # Step 2: Test direct API
    api_key = os.getenv("GEMINI_API_KEY")
    if not test_direct_api_call(api_key):
        print("\n❌ Direct API test failed")
        return False
    
    # Step 3: Test LangChain
    if not test_langchain_integration(llm):
        print("\n❌ LangChain integration test failed")
        return False
    
    # Step 4: Test CrewAI
    if not test_crewai_integration(llm):
        print("\n❌ CrewAI integration test failed")
        return False
    
    print("\n🎉 ALL DEBUG TESTS PASSED!")
    print("Your Gemini API configuration is working correctly!")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n💡 DEBUG SUMMARY:")
        print("- Check the detailed logs above for exact error details")
        print("- Verify your GEMINI_API_KEY is valid") 
        print("- Ensure you have internet connectivity")
        print("- Check for any API quota/billing issues")
    else:
        print("\n✅ Your setup is ready for production use!") 