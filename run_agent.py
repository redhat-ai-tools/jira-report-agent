#!/usr/bin/env python3
"""
Simple script to run the JIRA Report Agent
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    try:
        from src.agent import create_client, create_agent, run_task
        
        print("🚀 Starting JIRA Report Agent...")
        client = create_client()
        agent = create_agent(client)
        run_task(agent)
        print("✅ JIRA Report Agent completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running JIRA Report Agent: {e}")
        raise 