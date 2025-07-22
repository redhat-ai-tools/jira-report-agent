#!/usr/bin/env python3
"""
CrewAI-based JIRA Report Agent
Alternative implementation using CrewAI instead of Llama Stack
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from datetime import datetime, timedelta
import os
from typing import Dict, List, Any
import json

# Custom JIRA Tool for CrewAI
class JIRADataTool(BaseTool):
    name: str = "jira_data_fetcher"
    description: str = "Fetches JIRA issues from specified projects with filters for status and date ranges"
    
    def _run(self, project: str, status: str = "6", limit: int = 50) -> str:
        """
        Fetch JIRA issues for a specific project
        In real implementation, this would connect to the MCP server or JIRA API
        """
        # This is a placeholder - in real implementation you'd call:
        # - The MCP server functions we used before
        # - Direct JIRA API calls  
        # - Database queries, etc.
        
        # For demo purposes, returning mock data structure
        sample_data = {
            "project": project,
            "issues": [
                {
                    "key": f"{project}-123",
                    "summary": "Sample closed issue",
                    "priority": "10300", 
                    "resolution_date": "2025-01-15T10:30:00Z",
                    "status": status
                }
            ],
            "total_count": 1
        }
        return json.dumps(sample_data)

class DateFilterTool(BaseTool):
    name: str = "date_filter"
    description: str = "Filters issues based on resolution date within the last week"
    
    def _run(self, issues_json: str) -> str:
        """Filter issues to only include those from the last week"""
        try:
            data = json.loads(issues_json)
            week_ago = datetime.now() - timedelta(days=7)
            
            filtered_issues = []
            for issue in data.get("issues", []):
                if issue.get("resolution_date"):
                    # Parse resolution date and check if within last week
                    resolution_date = datetime.fromisoformat(issue["resolution_date"].replace('Z', '+00:00'))
                    if resolution_date >= week_ago:
                        filtered_issues.append(issue)
            
            data["issues"] = filtered_issues
            data["filtered_count"] = len(filtered_issues)
            return json.dumps(data)
        except Exception as e:
            return f"Error filtering dates: {e}"

def create_jira_report_crew():
    """Create a CrewAI crew for JIRA reporting"""
    
    # Initialize tools
    jira_tool = JIRADataTool()
    date_filter_tool = DateFilterTool()
    
    # Agent 1: Data Collector
    data_collector = Agent(
        role='JIRA Data Collector',
        goal='Efficiently collect JIRA issue data from specified projects',
        backstory="""You are a specialized data collection agent with expertise in 
        JIRA systems. Your job is to fetch comprehensive issue data from multiple 
        projects, ensuring you capture all relevant closed issues.""",
        tools=[jira_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 2: Data Analyst  
    data_analyst = Agent(
        role='Data Analysis Specialist',
        goal='Filter and analyze JIRA data based on time ranges and criteria',
        backstory="""You are a meticulous data analyst who specializes in temporal 
        analysis and filtering. You excel at identifying patterns and ensuring data 
        quality by applying precise date filters and validation.""",
        tools=[date_filter_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 3: Report Generator
    report_generator = Agent(
        role='Technical Report Writer',
        goal='Create clear, professional reports from JIRA data analysis',
        backstory="""You are an experienced technical writer who specializes in 
        creating clear, actionable reports. You transform raw data into insightful 
        summaries that help teams understand their issue resolution patterns.""",
        verbose=True,
        allow_delegation=True
    )
    
    # Task 1: Collect Data from Projects
    data_collection_task = Task(
        description="""
        Collect closed JIRA issues (status=6) from these projects:
        - CCITJEN
        - CCITRP  
        - QEHS
        
        For each project, fetch up to 50 closed issues. Ensure you capture:
        - Issue key and summary
        - Priority level
        - Resolution date
        - Current status
        
        Return the raw data for further analysis.
        """,
        expected_output="JSON data containing closed issues from all three projects",
        agent=data_collector
    )
    
    # Task 2: Filter Recent Issues
    analysis_task = Task(
        description="""
        Analyze the collected JIRA data and filter for issues resolved in the last 7 days.
        Apply date filtering to identify only the most recent closed issues.
        Validate the data quality and remove any invalid or incomplete records.
        """,
        expected_output="Filtered dataset containing only issues closed within the last week",
        agent=data_analyst
    )
    
    # Task 3: Generate Report
    report_task = Task(
        description="""
        Create a comprehensive weekly closed issues report based on the filtered data.
        
        The report should include:
        1. Executive summary of closed issues per project
        2. Detailed table with columns: Project, Issue Key, Summary, Priority, Resolution Date
        3. Summary statistics (total issues closed, issues per project)
        4. Any notable patterns or observations
        
        Format the report in a clear, professional manner suitable for stakeholders.
        If no issues are found for any project, explicitly mention this.
        """,
        expected_output="Professional weekly JIRA closed issues report in markdown format",
        agent=report_generator,
        output_file="reports/weekly_jira_report.md"
    )
    
    # Create the crew
    crew = Crew(
        agents=[data_collector, data_analyst, report_generator],
        tasks=[data_collection_task, analysis_task, report_task],
        process=Process.sequential,
        verbose=2
    )
    
    return crew

def main():
    """Run the CrewAI JIRA report agent"""
    
    # Set up environment (you'd set your LLM API keys here)
    # os.environ["OPENAI_API_KEY"] = "your-api-key"
    
    print("🚀 Starting CrewAI JIRA Report Agent...")
    
    # Create and run the crew
    crew = create_jira_report_crew()
    
    # Execute the reporting workflow
    result = crew.kickoff()
    
    print("\n" + "="*50)
    print("📊 JIRA REPORT COMPLETE")
    print("="*50)
    print(result)
            print("\n📁 Report saved to: reports/weekly_jira_report.md")

if __name__ == "__main__":
    main() 