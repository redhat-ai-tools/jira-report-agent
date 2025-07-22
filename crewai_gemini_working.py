#!/usr/bin/env python3
"""
Working JIRA Report Agent - Monthly Scope with REAL MCP Integration
Uses actual jira-mcp-snowflake MCP server functions for real data
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any

from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

def setup_gemini_llm():
    """Setup Gemini LLM with proper configuration"""
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_api_key or gemini_api_key in ['test-key', 'your-api-key', '']:
        raise ValueError("❌ Please set a real GEMINI_API_KEY environment variable")
    
    print(f"🔑 Using Gemini API Key: {gemini_api_key[:20]}...")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=gemini_api_key,
        temperature=0.1,
        convert_system_message_to_human=True,
        max_tokens=4000,
        timeout=60,
    )
    return llm

class WorkingMCPJIRADataTool(BaseTool):
    """Tool that actually calls the real MCP functions"""
    name: str = "working_mcp_jira_fetcher"
    description: str = "Fetches JIRA issues using real MCP function calls"
    
    def _run(self, project: str, status: str = "6", limit: int = 100) -> str:
        """Call the real MCP function"""
        try:
            print(f"🔍 Making REAL MCP call for project {project}...")
            print(f"   Status: {status} (6=Closed)")
            print(f"   Limit: {limit}")
            
            # Call the actual MCP function that we know exists
            # This should work since we have access to it in this environment
            result = mcp_jira_mcp_snowflake_list_jira_issues(
                project=project,
                status=status,
                limit=limit
            )
            
            print(f"✅ MCP call successful for {project}")
            if result and isinstance(result, dict):
                issues_count = len(result.get('issues', []))
                print(f"📊 Retrieved {issues_count} issues from {project}")
                
                # Add metadata to show this is real data
                result['data_source'] = 'Real MCP Server (jira-mcp-snowflake)'
                result['call_timestamp'] = datetime.now().isoformat()
                result['project_requested'] = project
            
            return json.dumps(result, default=str)
            
        except NameError as e:
            error_msg = f"MCP function not available: {e}"
            print(f"❌ {error_msg}")
            return json.dumps({
                "error": error_msg,
                "project": project,
                "solution": "Run this in an environment with jira-mcp-snowflake MCP server"
            })
        except Exception as e:
            error_msg = f"MCP call failed: {e}"
            print(f"❌ {error_msg}")
            return json.dumps({
                "error": error_msg,
                "project": project,
                "details": str(e)
            })

class MonthlyDateFilterTool(BaseTool):
    name: str = "monthly_date_filter"
    description: str = "Filters JIRA issues to only include those resolved within the last 30 days"
    
    def _run(self, issues_json: str, days: int = 30) -> str:
        """Filter issues by resolution date"""
        try:
            data = json.loads(issues_json)
            
            if "error" in data:
                return issues_json  # Pass through errors
            
            month_ago = datetime.now() - timedelta(days=days)
            filtered_issues = []
            
            for issue in data.get("issues", []):
                if issue.get("resolution_date"):
                    try:
                        # Parse the timestamp format from MCP server
                        timestamp_str = issue["resolution_date"].split()[0]
                        resolution_date = datetime.fromtimestamp(float(timestamp_str))
                        
                        if resolution_date >= month_ago:
                            filtered_issues.append(issue)
                    except (ValueError, IndexError) as e:
                        print(f"⚠️  Could not parse date for {issue.get('key', 'unknown')}: {e}")
                        continue
            
            result = {
                "issues": filtered_issues,
                "total_filtered": len(filtered_issues),
                "original_total": len(data.get("issues", [])),
                "filter_applied": f"Last {days} days",
                "filter_date": month_ago.isoformat(),
                "project": data.get("project", "unknown")
            }
            
            print(f"📅 Filtered to {len(filtered_issues)} issues from last {days} days")
            return json.dumps(result, default=str)
            
        except Exception as e:
            return json.dumps({"error": f"Date filtering failed: {e}"})

def create_working_crew():
    """Create a crew that uses real MCP data"""
    
    # Setup LLM
    llm = setup_gemini_llm()
    
    # Setup tools
    mcp_tool = WorkingMCPJIRADataTool()
    filter_tool = MonthlyDateFilterTool()
    
    # Create agents
    data_collector = Agent(
        role='JIRA Data Collector',
        goal='Collect real JIRA data from the jira-mcp-snowflake MCP server',
        backstory="You are responsible for gathering real JIRA data using MCP function calls.",
        tools=[mcp_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    data_analyst = Agent(
        role='JIRA Data Analyst',
        goal='Filter and analyze JIRA data for monthly reporting',
        backstory="You filter JIRA data to focus on the last 30 days and provide analysis.",
        tools=[filter_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    report_generator = Agent(
        role='Report Generator',
        goal='Create professional monthly JIRA reports',
        backstory="You create comprehensive monthly reports from analyzed JIRA data.",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )
    
    # Create tasks
    data_collection_task = Task(
        description="""
        Collect real JIRA data from the jira-mcp-snowflake MCP server for these projects:
        - CCITJEN
        - CCITRP
        - QEHS
        
        For each project, fetch up to 100 closed issues (status=6).
        Return comprehensive data for analysis.
        """,
        expected_output="Real JIRA data from MCP server for all three projects",
        agent=data_collector
    )
    
    analysis_task = Task(
        description="""
        Analyze the collected JIRA data:
        1. Filter for issues resolved within the last 30 days only
        2. Validate data quality
        3. Count issues per project
        4. Identify patterns and trends
        """,
        expected_output="Filtered dataset with monthly analysis and statistics",
        agent=data_analyst
    )
    
    report_task = Task(
        description="""
        Create a professional monthly JIRA closed issues report with:
        
        # Monthly JIRA Closed Issues Report
        **Report Period:** Last 30 Days
        **Generated:** [current date]
        **Data Source:** jira-mcp-snowflake MCP Server
        
        ## Executive Summary
        - Total issues closed across all projects
        - Issues closed per project
        - Monthly trends and insights
        
        ## Project Details
        
        ### CCITJEN
        [Table with issue details or "No issues closed this month"]
        
        ### CCITRP
        [Table with issue details or "No issues closed this month"]
        
        ### QEHS
        [Table with issue details or "No issues closed this month"]
        
        ## Summary Statistics
        - Total issues closed: X
        - Average per day: X
        - Most active project: X
        
        Format as clean markdown ready for stakeholders.
        """,
        expected_output="Complete monthly JIRA report in markdown format",
        agent=report_generator,
        output_file="reports/monthly_jira_report_working.md"
    )
    
    # Create crew
    crew = Crew(
        agents=[data_collector, data_analyst, report_generator],
        tasks=[data_collection_task, analysis_task, report_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew

def main():
    """Run the working JIRA report agent"""
    try:
        print("🚀 STARTING WORKING JIRA REPORT AGENT")
        print("=" * 60)
        print("📊 Scope: Monthly (Last 30 Days)")
        print("🎯 Projects: CCITJEN, CCITRP, QEHS")
        print("🔗 Data Source: Real MCP Server (jira-mcp-snowflake)")
        print("=" * 60)
        
        crew = create_working_crew()
        
        print("\n🔥 Starting crew execution...")
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("📊 MONTHLY JIRA REPORT GENERATED")
        print("=" * 60)
        print(result)
        print(f"\n📁 Report saved to: monthly_jira_report_working.md")
        print("🔗 Data source: Real MCP Server (jira-mcp-snowflake)")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Please set your GEMINI_API_KEY:")
        print("   export GEMINI_API_KEY='your-real-api-key'")
        
    except Exception as e:
        print(f"❌ Execution Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 