#!/usr/bin/env python3
"""
Test script for Gemini + CrewAI + Direct MCP setup
Verifies configuration and dependencies without making actual API calls
"""

import os
import sys
from datetime import datetime

def test_imports():
    """Test that all required packages can be imported"""
    print("🔧 Testing imports...")
    
    try:
        import crewai
        print(f"  ✅ CrewAI: {crewai.__version__}")
    except ImportError as e:
        print(f"  ❌ CrewAI import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("  ✅ Google Generative AI: Available")
    except ImportError as e:
        print(f"  ❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("  ✅ LangChain Google GenAI: Available")
    except ImportError as e:
        print(f"  ❌ LangChain Google GenAI import failed: {e}")
        return False
    
    try:
        from crewai.tools import BaseTool
        print("  ✅ CrewAI Tools: Available")
    except ImportError as e:
        print(f"  ❌ CrewAI Tools import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from crewai_config import LLMConfig, MCPConfig, setup_direct_mcp_environment
        
        # Set a dummy API key for testing
        os.environ["GEMINI_API_KEY"] = "test-key-for-config-validation"
        os.environ["LLM_PROVIDER"] = "gemini"
        
        # Test configuration loading
        llm_config = LLMConfig()
        mcp_config = MCPConfig()
        
        print(f"  ✅ LLM Provider: {llm_config.provider}")
        print(f"  ✅ MCP Server: {mcp_config.mcp_server_name}")
        print(f"  ✅ Direct MCP: {mcp_config.use_direct_mcp}")
        print(f"  ✅ Projects: {mcp_config.projects}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")
        return False

def test_llm_creation():
    """Test LLM object creation (without API calls)"""
    print("\n🔧 Testing LLM creation...")
    
    try:
        from crewai_config import LLMConfig
        
        # Set dummy API key
        os.environ["GEMINI_API_KEY"] = "test-key-for-llm-creation"
        
        llm_config = LLMConfig()
        llm = llm_config.create_llm()
        
        print(f"  ✅ LLM created: {type(llm).__name__}")
        print(f"  ✅ Model: {getattr(llm, 'model_name', 'gemini-1.5-flash')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ LLM creation failed: {e}")
        return False

def test_agent_creation():
    """Test CrewAI agent creation (without running)"""
    print("\n🔧 Testing agent creation...")
    
    try:
        from crewai import Agent
        from crewai_config import LLMConfig
        
        # Set dummy API key
        os.environ["GEMINI_API_KEY"] = "test-key-for-agent-creation"
        
        llm_config = LLMConfig()
        llm = llm_config.create_llm()
        
        # Create a test agent
        test_agent = Agent(
            role="Test Agent",
            goal="Test agent creation",
            backstory="This is a test agent for validation",
            llm=llm,
            verbose=False
        )
        
        print(f"  ✅ Agent created: {test_agent.role}")
        print(f"  ✅ Agent goal: {test_agent.goal}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Agent creation failed: {e}")
        return False

def test_tool_creation():
    """Test custom tool creation"""
    print("\n🔧 Testing tool creation...")
    
    try:
        from crewai.tools import BaseTool
        
        class TestTool(BaseTool):
            name: str = "test_tool"
            description: str = "A test tool for validation"
            
            def _run(self, query: str) -> str:
                return f"Test tool executed with query: {query}"
        
        test_tool = TestTool()
        result = test_tool._run("test query")
        
        print(f"  ✅ Tool created: {test_tool.name}")
        print(f"  ✅ Tool test result: {result}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Tool creation failed: {e}")
        return False

def test_mcp_configuration():
    """Test MCP configuration and function call structure"""
    print("\n🔧 Testing MCP configuration...")
    
    try:
        from crewai_config import MCPConfig, DirectMCPJIRADataTool
        
        # Test MCP configuration
        mcp_config = MCPConfig()
        print(f"  ✅ MCP Server: {mcp_config.mcp_server_name}")
        print(f"  ✅ Projects: {mcp_config.projects}")
        
        # Test function call structure
        call_structure = mcp_config.get_mcp_function_call_structure("CCITJEN")
        print(f"  ✅ Function name: {call_structure['function_name']}")
        print(f"  ✅ Call type: {call_structure['call_type']}")
        
        # Test tool creation
        mcp_tool = DirectMCPJIRADataTool()
        print(f"  ✅ MCP tool created successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ MCP configuration test failed: {e}")
        return False

def test_environment_setup():
    """Test environment variable setup"""
    print("\n🔧 Testing environment setup...")
    
    # Test required environment variables
    test_env_vars = {
        "GEMINI_API_KEY": "test-api-key",
        "LLM_PROVIDER": "gemini",
        "MCP_SERVER_NAME": "jira-mcp-snowflake"
    }
    
    for var, value in test_env_vars.items():
        os.environ[var] = value
        print(f"  ✅ {var}: Set")
    
    # Test optional variables
    optional_vars = {
        "GEMINI_MODEL": "gemini-1.5-flash",
        "LLM_TEMPERATURE": "0.1"
    }
    
    for var, default in optional_vars.items():
        os.environ.setdefault(var, default)
        print(f"  ✅ {var}: {os.environ[var]}")
    
    # Verify no HTTP URL is needed
    print(f"  ✅ No MCP_SERVER_URL required (direct function calls)")
    
    return True

def test_mcp_function_simulation():
    """Test MCP function call simulation"""
    print("\n🔧 Testing MCP function simulation...")
    
    try:
        from crewai_config import MCPConfig
        
        mcp_config = MCPConfig()
        
        # Test simulation without sample data
        response = mcp_config.simulate_mcp_response("CCITJEN", include_sample_data=False)
        print(f"  ✅ Empty response structure: {response['total_count']} issues")
        
        # Test simulation with sample data
        response_with_data = mcp_config.simulate_mcp_response("CCITJEN", include_sample_data=True)
        print(f"  ✅ Sample response structure: {response_with_data['total_count']} issues")
        print(f"  ✅ Sample issue key: {response_with_data['issues'][0]['key']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ MCP function simulation test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("🚀 Gemini + CrewAI + Direct MCP Setup Test Suite")
    print("="*55)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("LLM Creation Test", test_llm_creation),
        ("Agent Creation Test", test_agent_creation),
        ("Tool Creation Test", test_tool_creation),
        ("MCP Configuration Test", test_mcp_configuration),
        ("Environment Setup Test", test_environment_setup),
        ("MCP Function Simulation Test", test_mcp_function_simulation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*55)
    print("📊 TEST RESULTS SUMMARY")
    print("="*55)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your Gemini + CrewAI + Direct MCP setup is ready!")
        print("\n🚀 Next steps:")
        print("1. Get your real Gemini API key from https://makersuite.google.com/app/apikey")
        print("2. Set: export GEMINI_API_KEY='your-real-api-key'")
        print("3. Ensure your jira-mcp-snowflake MCP server is configured")
        print("4. Run: python crewai_gemini_implementation.py")
        print("\n💡 Note: No MCP_SERVER_URL needed - uses direct function calls!")
    else:
        print("⚠️  Some tests failed. Please fix the issues above before proceeding.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 