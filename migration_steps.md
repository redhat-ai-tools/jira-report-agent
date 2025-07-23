# Migration from Llama Stack to CrewAI

## Step 1: Install CrewAI
```bash
pip install crewai
pip install openai  # or your preferred LLM provider
```

## Step 2: Environment Setup
```bash
# Copy your existing environment variables
export OPENAI_API_KEY="your-api-key"
export USE_MCP_SERVER="true"  # Keep using your MCP server
export MCP_SERVER_URL="http://localhost:8000"
```

## Step 3: Integrate MCP Functions
```python
# Use the MCP functions we already tested:
from crewai_config import RealJIRADataTool

# This will call your jira-mcp-snowflake server
tool = RealJIRADataTool()
result = tool.fetch_closed_issues("CCITJEN")
```

## Step 4: Run CrewAI Version
```bash
python crewai_implementation_example.py
```

## Benefits You'll Get:
- ✅ Same JIRA data access (via MCP)
- ✅ Better structured workflow
- ✅ Easier to extend and maintain
- ✅ More sophisticated reporting capabilities
- ✅ No Llama Stack dependency
