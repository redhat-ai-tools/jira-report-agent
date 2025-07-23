#!/usr/bin/env python3
"""
Debug CrewAI Execution - Find where "unknown error occurred" happens
"""

import os
import sys
import traceback
from datetime import datetime
import json
from typing import Dict, List, Any

# Import CrewAI components
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

def debug_llm_setup():
    """Debug LLM setup with detailed logging"""
    
    print("🔍 DEBUG: LLM Setup")
    print("-" * 30)
    
    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        print(f"✅ API Key found: {gemini_api_key is not None}")
        
        if gemini_api_key == "test-key":
            print("❌ Using test-key (not valid)")
            return None
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.1,
            convert_system_message_to_human=True,
        )
        
        print("✅ LLM created successfully")
        return llm
        
    except Exception as e:
        print(f"❌ LLM setup failed: {e}")
        traceback.print_exc()
        return None

class DebugMCPTool(BaseTool):
    """Debug version of MCP tool with detailed logging"""
    name: str = "debug_mcp_tool"
    description: str = "Debug MCP tool with detailed logging"
    
    def _run(self, project: str = "TEST") -> str:
        print(f"🔧 DEBUG: Tool execution for project {project}")
        try:
            result = {
                "project": project,
                "status": "success",
                "message": f"Tool executed successfully for {project}",
                "timestamp": datetime.now().isoformat()
            }
            print(f"✅ Tool execution successful")
            return json.dumps(result)
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            traceback.print_exc()
            return json.dumps({"error": str(e), "project": project})

def debug_agent_creation(llm):
    """Debug agent creation with detailed logging"""
    
    print("\n🔍 DEBUG: Agent Creation")
    print("-" * 30)
    
    try:
        tool = DebugMCPTool()
        print("✅ Tool created")
        
        agent = Agent(
            role='Debug Agent',
            goal='Test agent creation and execution',
            backstory='A debug agent to test the execution flow',
            tools=[tool],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            max_iter=1  # Limit iterations for debugging
        )
        
        print("✅ Agent created successfully")
        print(f"   Role: {agent.role}")
        print(f"   LLM type: {type(agent.llm).__name__}")
        print(f"   Tools count: {len(agent.tools)}")
        
        return agent
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        traceback.print_exc()
        return None

def debug_task_creation(agent):
    """Debug task creation with detailed logging"""
    
    print("\n🔍 DEBUG: Task Creation")
    print("-" * 30)
    
    try:
        task = Task(
            description="Simply say hello and confirm you are working. Use the debug tool if needed.",
            expected_output="A simple hello message confirming the agent is working",
            agent=agent
        )
        
        print("✅ Task created successfully")
        print(f"   Description: {task.description[:50]}...")
        print(f"   Agent: {task.agent.role}")
        
        return task
        
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        traceback.print_exc()
        return None

def debug_crew_creation(agent, task):
    """Debug crew creation with detailed logging"""
    
    print("\n🔍 DEBUG: Crew Creation")
    print("-" * 30)
    
    try:
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        print("✅ Crew created successfully")
        print(f"   Agents count: {len(crew.agents)}")
        print(f"   Tasks count: {len(crew.tasks)}")
        print(f"   Process: {crew.process}")
        
        return crew
        
    except Exception as e:
        print(f"❌ Crew creation failed: {e}")
        traceback.print_exc()
        return None

def debug_crew_execution(crew):
    """Debug crew execution with detailed logging to find where error occurs"""
    
    print("\n🔍 DEBUG: Crew Execution")
    print("-" * 30)
    
    try:
        print("🚀 Starting crew kickoff...")
        print("📍 Execution stage: Pre-kickoff")
        
        # This is where the "unknown error occurred" likely happens
        result = crew.kickoff()
        
        print("📍 Execution stage: Post-kickoff")
        print("✅ Crew execution completed successfully")
        print(f"📊 Result: {result}")
        
        return result
        
    except Exception as e:
        print(f"📍 Execution stage: Exception caught")
        print(f"❌ Crew execution failed: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        print(f"🔍 Error message: '{str(e)}'")
        
        # Check if this is the "unknown error occurred" message
        if "unknown error occurred" in str(e).lower():
            print("🎯 FOUND IT! This is where 'unknown error occurred' comes from")
            print("💡 This suggests the error is happening inside CrewAI's execution engine")
        
        # Print full traceback to see the call stack
        print("\n📋 Full traceback:")
        traceback.print_exc()
        
        return None

def debug_step_by_step():
    """Run step-by-step debugging to identify exactly where the error occurs"""
    
    print("🐛 CREWAI EXECUTION DEBUG")
    print("=" * 50)
    print("🎯 Goal: Find where 'unknown error occurred' happens")
    print("=" * 50)
    
    # Step 1: LLM setup
    llm = debug_llm_setup()
    if not llm:
        print("❌ Cannot proceed - LLM setup failed")
        return False
    
    # Step 2: Agent creation
    agent = debug_agent_creation(llm)
    if not agent:
        print("❌ Cannot proceed - Agent creation failed")
        return False
    
    # Step 3: Task creation
    task = debug_task_creation(agent)
    if not task:
        print("❌ Cannot proceed - Task creation failed")
        return False
    
    # Step 4: Crew creation
    crew = debug_crew_creation(agent, task)
    if not crew:
        print("❌ Cannot proceed - Crew creation failed")
        return False
    
    # Step 5: Crew execution (this is likely where the error occurs)
    result = debug_crew_execution(crew)
    
    if result:
        print("\n🎉 SUCCESS: All steps completed without 'unknown error occurred'")
        return True
    else:
        print("\n💥 FAILURE: Found where 'unknown error occurred' happens")
        return False

def analyze_crewai_error_sources():
    """Analyze common sources of CrewAI 'unknown error occurred' messages"""
    
    print("\n📚 COMMON SOURCES OF 'UNKNOWN ERROR OCCURRED':")
    print("=" * 50)
    print()
    print("1. 🤖 LLM Connection Issues:")
    print("   - Invalid API key")
    print("   - Network connectivity")
    print("   - API rate limits/quota")
    print("   - Model not available")
    print()
    print("2. 📋 Task Execution Issues:")
    print("   - Agent can't understand the task")
    print("   - Tool execution failures")
    print("   - Max iterations exceeded")
    print("   - Memory/context issues")
    print()
    print("3. 🔧 Tool Issues:")
    print("   - Tool import failures")
    print("   - Tool execution exceptions")
    print("   - Tool return format issues")
    print()
    print("4. 🏗️ CrewAI Framework Issues:")
    print("   - Agent configuration problems")
    print("   - Task dependencies")
    print("   - Process execution failures")
    print()
    print("💡 The debug execution above will help identify which category!")

if __name__ == "__main__":
    print("🔬 Starting CrewAI Debug Session")
    print("Looking for 'unknown error occurred' source...")
    print()
    
    success = debug_step_by_step()
    
    print("\n" + "=" * 50)
    
    if success:
        print("✅ No 'unknown error occurred' found in this debug run")
        print("💡 The error might be in your specific configuration")
        print("   Try running your actual agent to reproduce the error")
    else:
        print("🎯 Found the source of 'unknown error occurred'!")
        print("📋 Check the debug output above for details")
    
    analyze_crewai_error_sources()
    
    print("\n🔍 Next Steps:")
    print("1. Check the specific error details above")
    print("2. Verify your GEMINI_API_KEY is valid") 
    print("3. Run: python test_gemini_api_key.py")
    print("4. Share the specific error traceback for more help") 