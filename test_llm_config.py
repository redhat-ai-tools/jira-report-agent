#!/usr/bin/env python3
"""
Simple test to identify LLM configuration issues
"""

import os
from datetime import datetime

def test_llm_configuration():
    """Test LLM configuration step by step"""
    
    print("🔍 TESTING CREWAI + GEMINI LLM CONFIGURATION")
    print("=" * 50)
    
    # Step 1: Check environment
    print("📋 Step 1: Environment Check")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        if gemini_key == "test-key":
            print("❌ GEMINI_API_KEY is set to 'test-key' (not valid)")
            print("💡 Get a real API key from: https://makersuite.google.com/app/apikey")
            return False
        else:
            print(f"✅ GEMINI_API_KEY is set: {'*' * 20}")
    else:
        print("❌ GEMINI_API_KEY not set")
        print("💡 Set it with: export GEMINI_API_KEY='your-real-api-key'")
        return False
    
    # Step 2: Test imports
    print("\n📦 Step 2: Import Test")
    try:
        from crewai import Agent, Task, Crew, Process
        from crewai.tools import BaseTool
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Step 3: Test LLM creation
    print("\n🤖 Step 3: LLM Creation Test")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_key,
            temperature=0.1,
            convert_system_message_to_human=True,
        )
        print("✅ LLM created successfully")
        print(f"   Model: {llm.model}")
        print(f"   Temperature: {llm.temperature}")
    except Exception as e:
        print(f"❌ LLM creation failed: {e}")
        return False
    
    # Step 4: Test Agent creation
    print("\n👤 Step 4: Agent Creation Test")
    try:
        test_agent = Agent(
            role='Test Agent',
            goal='Test LLM configuration',
            backstory='A simple test agent to verify LLM setup.',
            llm=llm,
            verbose=True
        )
        print("✅ Agent created successfully")
        print(f"   Role: {test_agent.role}")
        print(f"   LLM type: {type(test_agent.llm).__name__}")
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False
    
    # Step 5: Test simple task
    print("\n📋 Step 5: Simple Task Test")
    try:
        test_task = Task(
            description="Say hello and confirm the LLM is working",
            expected_output="A simple greeting message",
            agent=test_agent
        )
        print("✅ Task created successfully")
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return False
    
    # Step 6: Test crew creation  
    print("\n👥 Step 6: Crew Creation Test")
    try:
        test_crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            verbose=True
        )
        print("✅ Crew created successfully")
    except Exception as e:
        print(f"❌ Crew creation failed: {e}")
        return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Your LLM configuration is working correctly.")
    print("\nTo test actual execution:")
    print("1. Make sure GEMINI_API_KEY is set to a real API key")
    print("2. Run: python crewai_gemini_implementation_real.py")
    
    return True

if __name__ == "__main__":
    success = test_llm_configuration()
    if not success:
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Get Gemini API key: https://makersuite.google.com/app/apikey")  
        print("2. Set environment: export GEMINI_API_KEY='your-real-key'")
        print("3. Install packages: pip install crewai langchain-google-genai")
        print("4. Run this test again") 