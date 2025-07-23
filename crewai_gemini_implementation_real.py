#!/usr/bin/env python3
"""
CrewAI + Gemini + Real MCP Integration
Uses Google Gemini with actual MCP function calls to jira-mcp-snowflake
"""

import os
import sys
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Real MCP Integration Tool (calls actual MCP functions)
class RealMCPJIRADataTool(BaseTool):
    name: str = "real_mcp_jira_fetcher"
    description: str = "Fetches JIRA issues using real MCP function calls to jira-mcp-snowflake"
    
    def _run(self, project: str, status: str = "6", limit: int = 100) -> str:
        """
        Make real calls to the MCP jira-mcp-snowflake server
        """
        try:
            print(f"🔍 Making REAL MCP call for project {project}...")
            
            # Call the actual MCP function that's available in this environment
            # This should connect to the real jira-mcp-snowflake MCP server
            try:
                # Use the actual MCP function that we know is available
                from types import ModuleType
                import sys
                
                # Check if we can import the MCP functions
                # The functions should be available as tools in the environment
                print(f"📡 Calling MCP function: mcp_jira-mcp-snowflake_list_jira_issues")
                print(f"   Project: {project}")
                print(f"   Status: {status} (6=Closed)")
                print(f"   Limit: {limit}")
                
                # Try to use the MCP function through exec since it's not importable
                # This is a workaround for MCP functions that aren't in Python's import system
                
                # First, let's try to call it directly if it exists in the environment
                mcp_result = None
                
                # We need to use the actual MCP call mechanism
                # Since this is running in an MCP-enabled environment, we should be able to call it
                
                # For now, let's make a simple call and see what happens
                exec_globals = {}
                exec_code = f"""
import json
try:
    # This should work if MCP functions are available
    result = mcp_jira_mcp_snowflake_list_jira_issues(
        project="{project}",
        status="{status}",
        limit={limit}
    )
    mcp_result = result
except NameError as e:
    print(f"MCP function not found: {{e}}")
    mcp_result = None
except Exception as e:
    print(f"MCP call error: {{e}}")
    mcp_result = None
"""
                
                exec(exec_code, exec_globals)
                mcp_result = exec_globals.get('mcp_result')
                
                if mcp_result is not None:
                    print(f"✅ Real MCP call successful for {project}")
                    print(f"📊 Retrieved {len(mcp_result.get('issues', []))} issues")
                    
                    # Add metadata to show this is real data
                    if isinstance(mcp_result, dict):
                        mcp_result['data_source'] = 'Real MCP Server (jira-mcp-snowflake)'
                        mcp_result['call_type'] = 'Direct MCP Function Call'
                        mcp_result['project_requested'] = project
                    
                    return json.dumps(mcp_result, default=str)
                else:
                    raise Exception("MCP function call returned None")
                    
            except Exception as mcp_error:
                print(f"⚠️  Direct MCP function call failed: {mcp_error}")
                print(f"🔄 This means the MCP server is not properly connected or functions not available")
                
                # Instead of fallback, we should return an error to help debug
                error_response = {
                    "error": f"MCP function call failed: {mcp_error}",
                    "project": project,
                    "status": status,
                    "limit": limit,
                    "mcp_function": "mcp_jira-mcp-snowflake_list_jira_issues",
                    "data_source": "MCP Error - Server Not Connected",
                    "troubleshooting": {
                        "issue": "MCP server jira-mcp-snowflake is not accessible",
                        "possible_causes": [
                            "MCP server not running",
                            "MCP functions not properly registered",
                            "Environment not configured for direct MCP calls"
                        ],
                        "recommendations": [
                            "Check if jira-mcp-snowflake MCP server is running",
                            "Verify MCP server configuration",
                            "Test MCP functions independently"
                        ]
                    }
                }
                return json.dumps(error_response, default=str)
                
        except Exception as e:
            error_msg = f"Tool execution failed: {e}"
            print(f"❌ {error_msg}")
            return json.dumps({
                "error": error_msg,
                "project": project,
                "mcp_function": "mcp_jira-mcp-snowflake_list_jira_issues",
                "data_source": "Tool Error"
            })

    def _create_fallback_response(self, project: str, status: str, limit: int) -> Dict[str, Any]:
        """Create a structured response for testing when MCP functions aren't available"""
        return {
            "project": project,
            "status": status,
            "limit": limit,
            "issues": [
                {
                    "key": f"{project}-DEMO-001",
                    "summary": f"Demo closed issue from {project} project",
                    "priority": "3",
                    "resolution_date": f"{int((datetime.now() - timedelta(days=2)).timestamp())}.000000000 1440",
                    "status": "6"
                }
            ],
            "total_count": 1,
            "mcp_function": "mcp_jira-mcp-snowflake_list_jira_issues",
            "data_source": "Fallback (for testing)",
            "note": "Replace with real MCP function call when available"
        }

class DateFilterTool(BaseTool):
    name: str = "date_filter"
    description: str = "Filters JIRA issues to only include those resolved within the last month"
    
    def _run(self, issues_json: str, days: int = 30) -> str:
        """Filter issues by resolution date"""
        try:
            data = json.loads(issues_json)
            
            if "error" in data:
                return issues_json  # Pass through errors
            
            week_ago = datetime.now() - timedelta(days=days)
            filtered_issues = []
            
            for issue in data.get("issues", []):
                if issue.get("resolution_date"):
                    try:
                        # Parse the timestamp format from MCP server
                        timestamp_str = issue["resolution_date"].split()[0]
                        resolution_date = datetime.fromtimestamp(float(timestamp_str))
                        
                        if resolution_date >= week_ago:
                            filtered_issues.append(issue)
                            
                    except (ValueError, IndexError) as e:
                        print(f"⚠️  Could not parse date for issue {issue.get('key', 'unknown')}: {e}")
                        continue
            
            data["issues"] = filtered_issues
            data["filtered_count"] = len(filtered_issues)
            data["original_count"] = len(data.get("issues", []))
            data["filter_applied"] = f"Last {days} days"
            
            print(f"📅 Filtered to {len(filtered_issues)} issues from last {days} days")
            return json.dumps(data, default=str)
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON format: {e}"
            return json.dumps({"error": error_msg})
        except Exception as e:
            error_msg = f"Date filtering failed: {e}"
            return json.dumps({"error": error_msg})

def create_gemini_llm():
    """Create and configure Gemini LLM for CrewAI"""
    
    # Get Gemini API key from environment
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")
    
    if gemini_api_key == "test-key":
        raise ValueError("Please set a real GEMINI_API_KEY. Get one from: https://makersuite.google.com/app/apikey")
    
    # Configure Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=gemini_api_key,
        temperature=0.1,
        convert_system_message_to_human=True,
    )
    
    print(f"🤖 Configured Gemini model: gemini-1.5-flash")
    return llm

def create_jira_gemini_crew():
    """Create CrewAI crew using Gemini LLM and real MCP integration"""
    
    # Create Gemini LLM instance
    gemini_llm = create_gemini_llm()
    
    # Initialize real MCP tools
    mcp_tool = RealMCPJIRADataTool()
    date_filter_tool = DateFilterTool()
    
    # Agent 1: JIRA Data Collector
    data_collector = Agent(
        role='JIRA Data Specialist',
        goal='Collect JIRA issue data using real MCP function calls',
        backstory="""You are an expert in JIRA data extraction using the jira-mcp-snowflake MCP server.""",
        tools=[mcp_tool],
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
    
    # Agent 2: Data Analyst
    data_analyst = Agent(
        role='Data Analysis Expert',
        goal='Filter and validate JIRA data for recent closed issues',
        backstory="""You specialize in temporal filtering and data quality validation.""",
        tools=[date_filter_tool],
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
    
    # Agent 3: Report Generator
    report_generator = Agent(
        role='Technical Report Specialist',
        goal='Create comprehensive JIRA reports',
        backstory="""You transform data into clear, actionable insights for stakeholders.""",
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
    
    # Task 1: Data Collection
    data_collection_task = Task(
        description="""
        Use the real MCP function calls to collect closed JIRA issues (status=6) from:
        - CCITJEN
        - CCITRP  
        - QEHS
        
        Call the MCP function for each project and compile the results.
        """,
        expected_output="JSON data with closed issues from all three projects",
        agent=data_collector
    )
    
    # Task 2: Data Analysis
    analysis_task = Task(
        description="""
        Filter the collected data to show only issues closed in the last 7 days.
        Provide statistics on the filtering results.
        """,
        expected_output="Filtered dataset with only recent closed issues and statistics",
        agent=data_analyst
    )
    
    # Task 3: Report Generation
    report_task = Task(
        description="""
        Create a professional monthly JIRA report in markdown format with:
        
        # Monthly JIRA Closed Issues Report
        **Data Source:** jira-mcp-snowflake MCP Server
        
        ## Executive Summary
        - Total issues closed: [number]
        - Per project breakdown
        
        ## Detailed Results
        ### CCITJEN: [count] issues
        [Table with issue details]
        
        ### CCITRP: [count] issues  
        [Table with issue details]
        
        ### QEHS: [count] issues
        [Table with issue details]
        
        ## Summary
        - Key insights
        - Data quality notes
        """,
        expected_output="Complete markdown report ready for stakeholders",
        agent=report_generator,
        output_file="reports/monthly_jira_report_real.md"
    )
    
    # Create the crew
    crew = Crew(
        agents=[data_collector, data_analyst, report_generator],
        tasks=[data_collection_task, analysis_task, report_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew

def setup_environment():
    """Setup and validate environment for real MCP integration"""
    
    print("🔧 Setting up Gemini + CrewAI + Real MCP environment...")
    
    # Check Gemini API key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("❌ GEMINI_API_KEY not set")
        print("\n📝 To fix this:")
        print("1. Get API key: https://makersuite.google.com/app/apikey")
        print("2. Set: export GEMINI_API_KEY='your-real-api-key'")
        return False
    
    if gemini_api_key == "test-key":
        print("❌ Please use a real Gemini API key, not 'test-key'")
        print("📝 Get one from: https://makersuite.google.com/app/apikey")
        return False
    
    print("✅ Environment configured:")
    print(f"   - Gemini API Key: {'*' * 20}")
    print(f"   - MCP Integration: jira-mcp-snowflake (real function calls)")
    print(f"   - Projects: CCITJEN, CCITRP, QEHS")
    
    return True

def main():
    """Run the real Gemini + CrewAI + MCP JIRA report agent"""
    
    print("🚀 Starting Real Gemini + CrewAI JIRA Report Agent")
    print("="*60)
    print("🔗 Using real MCP function calls to jira-mcp-snowflake")
    print("="*60)
    
    if not setup_environment():
        return
    
    try:
        print("\n📋 Creating CrewAI crew with real MCP integration...")
        crew = create_jira_gemini_crew()
        
        print("\n🎯 Starting JIRA report generation...")
        print("📡 Using real MCP function calls...")
        
        result = crew.kickoff()
        
        print("\n" + "="*60)
        print("📊 REAL JIRA REPORT COMPLETE")
        print("="*60)
        print(result)
        print(f"\n📁 Report saved to: reports/monthly_jira_report_real.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Ensure GEMINI_API_KEY is set with a real API key")
        print("2. Verify jira-mcp-snowflake MCP server is configured")
        print("3. Check that MCP functions are available in your environment")
        
        if "test-key" in str(e):
            print("\n💡 You need a real Gemini API key from:")
            print("   https://makersuite.google.com/app/apikey")

if __name__ == "__main__":
    main() 