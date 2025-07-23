# 🚀 Quick Start: Gemini + CrewAI + Direct MCP

This is the **fastest way** to get your JIRA report agent running with **Google Gemini** and your locally configured **jira-mcp-snowflake** MCP server.

## ⚡ 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements_crewai.txt

# 2. Get Gemini API key (free): https://makersuite.google.com/app/apikey

# 3. Set environment variable (only one needed!)
export GEMINI_API_KEY="your-actual-gemini-api-key"

# 4. Test setup
python test_gemini_setup.py

# 5. Run the agent
python crewai_gemini_implementation.py
```

## 📁 What You Get

### **Files Created:**
- `crewai_gemini_implementation.py` - Main agent with Gemini LLM
- `crewai_config.py` - Configuration manager (direct MCP calls)
- `requirements_crewai.txt` - Dependencies
- `test_gemini_setup.py` - Test suite

### **Architecture:**
```
Gemini LLM → CrewAI Agents → Direct MCP Calls → jira-mcp-snowflake → JIRA Data
```

### **3 Specialized Agents:**
1. **🔍 Data Collector** - Fetches JIRA issues via direct MCP function calls
2. **📊 Data Analyst** - Filters to last 7 days
3. **📝 Report Generator** - Creates markdown report

## 🎯 Output

**Generated Report:** `weekly_jira_report_gemini.md`

```markdown
# Weekly JIRA Closed Issues Report
**Report Period:** [Date Range]
**Data Source:** jira-mcp-snowflake MCP Server (Local)

## Executive Summary
- Total issues closed: X
- CCITJEN: X issues
- CCITRP: X issues  
- QEHS: X issues

## Detailed Results
[Professional tables with issue details]

## Technical Notes
- MCP Server: jira-mcp-snowflake (locally configured)
- Data retrieval method: Direct MCP function calls
```

## 🔧 Configuration Options

```bash
# Model selection
export GEMINI_MODEL="gemini-1.5-flash"    # Fast & cheap (default)
export GEMINI_MODEL="gemini-1.5-pro"      # More capable

# Temperature (0.0-1.0)
export LLM_TEMPERATURE="0.1"              # Consistent (default)

# Switch LLM provider
export LLM_PROVIDER="gemini"               # Default
export LLM_PROVIDER="openai"               # Alternative
```

## 🚨 Troubleshooting

### Common Issues:

**1. Import Error**
```bash
pip install -r requirements_crewai.txt
```

**2. API Key Error**
```bash
export GEMINI_API_KEY="your-real-key-here"
```

**3. MCP Function Not Available**
```bash
# Verify your locally configured MCP server
echo "jira-mcp-snowflake should be configured in your environment"

# The implementation will show which MCP functions it's trying to call:
# mcp_jira-mcp-snowflake_list_jira_issues
```

**4. No MCP_SERVER_URL Needed**
- ✅ This implementation uses **direct MCP function calls**
- ❌ No HTTP endpoints or server URLs required
- 🔗 Works with locally configured `jira-mcp-snowflake`

## ✅ Verification

Run the test suite:
```bash
python test_gemini_setup.py
```

Expected output:
```
🎉 All tests passed! Your Gemini + CrewAI + MCP setup is ready!
```

Test configuration:
```bash
python crewai_config.py
```

Expected output:
```
✅ Environment configured for GEMINI + Direct MCP integration
- MCP Server: jira-mcp-snowflake  
- Connection Type: Direct function calls
```

## 🔄 Migration Benefits

**From HTTP MCP Server → Direct MCP Calls:**
- ✅ **Simpler Setup** - No server URLs needed
- ✅ **Better Performance** - Direct function calls
- ✅ **Same Data Access** - Your jira-mcp-snowflake server works unchanged
- ✅ **Enhanced Architecture** - Multi-agent collaboration  
- ✅ **Cost Effective** - Gemini Flash is very affordable

## 🎁 Example Commands

```bash
# Basic run
python crewai_gemini_implementation.py

# Test without running
python test_gemini_setup.py

# Test configuration and see MCP details
python crewai_config.py

# Switch to Pro model for complex analysis
export GEMINI_MODEL="gemini-1.5-pro"
python crewai_gemini_implementation.py
```

## 📊 Cost Estimate

**Gemini 1.5 Flash** (default):
- Input: $0.075 per 1M tokens
- Output: $0.30 per 1M tokens
- **Typical report cost: <$0.01**

## 🔗 MCP Integration Details

The implementation uses **direct MCP function calls**:

```python
# Function called for each project:
mcp_jira-mcp-snowflake_list_jira_issues(
    project="CCITJEN",    # or CCITRP, QEHS
    status="6",           # Closed status
    limit=50              # Max issues to fetch
)
```

**Projects queried:**
- CCITJEN
- CCITRP  
- QEHS

**Connection type:** Direct function calls (no HTTP)

---

**🎉 You're ready!** Just set your Gemini API key and run the agent - no MCP server URL configuration needed! 