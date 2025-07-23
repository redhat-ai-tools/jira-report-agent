#!/usr/bin/env python3
"""
Specific Gemini API Key Test
Tests if your GEMINI_API_KEY is valid and working
"""

import os
import sys
from datetime import datetime

def test_gemini_api_key():
    """Test Gemini API key with actual API calls"""
    
    print("🔑 GEMINI API KEY VALIDATION TEST")
    print("=" * 50)
    print(f"🕐 Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Check environment variable
    print("📋 Step 1: Environment Variable Check")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in environment")
        print("💡 Set it with: export GEMINI_API_KEY='your-api-key'")
        return False
    
    if gemini_key == "test-key":
        print("❌ GEMINI_API_KEY is set to 'test-key' (placeholder)")
        print("💡 Get real key from: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"✅ GEMINI_API_KEY found: {gemini_key[:10]}...{gemini_key[-10:]}")
    print(f"   Length: {len(gemini_key)} characters")
    
    # Step 2: Test imports
    print("\n📦 Step 2: Import Test")
    try:
        import google.generativeai as genai
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ Google AI packages imported successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Install with: pip install google-generativeai langchain-google-genai")
        return False
    
    # Step 3: Test direct Google AI API
    print("\n🤖 Step 3: Direct Google AI API Test")
    try:
        # Configure direct API
        genai.configure(api_key=gemini_key)
        
        # List available models
        print("📋 Available models:")
        models = genai.list_models()
        model_names = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                model_names.append(model.name)
                print(f"   ✅ {model.name}")
        
        if not model_names:
            print("❌ No available models found")
            return False
            
    except Exception as e:
        print(f"❌ Direct API test failed: {e}")
        if "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower():
            print("💡 Your API key appears to be invalid")
            print("   Get a new one from: https://makersuite.google.com/app/apikey")
        elif "quota" in str(e).lower() or "billing" in str(e).lower():
            print("💡 API quota/billing issue - check your Google Cloud account")
        else:
            print("💡 Check your internet connection and API key")
        return False
    
    # Step 4: Test simple generation
    print("\n💬 Step 4: Simple Generation Test")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello and confirm you're working!")
        
        print("✅ Generation test successful!")
        print(f"📝 Response: {response.text[:100]}...")
        
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return False
    
    # Step 5: Test LangChain integration
    print("\n🔗 Step 5: LangChain Integration Test")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_key,
            temperature=0.1,
            convert_system_message_to_human=True,
        )
        
        # Test simple invoke
        response = llm.invoke("Hello! Please confirm you're working correctly.")
        print("✅ LangChain integration successful!")
        print(f"📝 Response: {response.content[:100]}...")
        
    except Exception as e:
        print(f"❌ LangChain integration failed: {e}")
        return False
    
    # Step 6: Test CrewAI compatibility
    print("\n👥 Step 6: CrewAI Compatibility Test")
    try:
        from crewai import Agent
        
        test_agent = Agent(
            role='Test Agent',
            goal='Test API connectivity',
            backstory='A test agent to verify Gemini API integration.',
            llm=llm,
            verbose=False
        )
        
        print("✅ CrewAI agent creation successful!")
        print(f"   Agent role: {test_agent.role}")
        print(f"   LLM type: {type(test_agent.llm).__name__}")
        
    except Exception as e:
        print(f"❌ CrewAI compatibility test failed: {e}")
        return False
    
    print("\n🎉 ALL GEMINI API TESTS PASSED!")
    print("Your Gemini API key is working perfectly!")
    print()
    print("✅ Summary:")
    print("  • API key format: Valid")
    print("  • Google AI access: Working")
    print("  • Content generation: Successful")  
    print("  • LangChain integration: Working")
    print("  • CrewAI compatibility: Ready")
    print()
    print("🚀 You can now run your CrewAI agents with confidence!")
    
    return True

def show_api_key_info():
    """Show information about getting and setting up Gemini API key"""
    
    print("\n📚 GEMINI API KEY SETUP GUIDE")
    print("=" * 40)
    print()
    print("🔗 Get API Key:")
    print("   https://makersuite.google.com/app/apikey")
    print()
    print("🔧 Set Environment Variable:")
    print("   export GEMINI_API_KEY='your-actual-api-key'")
    print()
    print("📋 Verify Setup:")
    print("   echo $GEMINI_API_KEY")
    print()
    print("🔒 Security Notes:")
    print("   • Keep your API key private")
    print("   • Don't commit it to version control")
    print("   • Use environment variables")
    print("   • Consider using .env files for development")
    print()
    print("💰 Cost Information:")
    print("   • Gemini 1.5 Flash has a generous free tier")
    print("   • Monitor usage in Google AI Studio")
    print("   • Check quotas and billing settings")

if __name__ == "__main__":
    print("🧪 Starting Gemini API Key Test...")
    print()
    
    success = test_gemini_api_key()
    
    if not success:
        print("\n" + "=" * 50)
        show_api_key_info()
    else:
        print("\n💡 Next Steps:")
        print("   1. Run: python crewai_gemini_fixed.py")
        print("   2. Your JIRA agent is ready to go!") 