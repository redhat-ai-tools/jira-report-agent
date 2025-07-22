# JIRA Report Agent

This agent provides automated JIRA issue reporting using the `jira-mcp-snowflake` MCP server. It creates reports of closed JIRA issues from specified projects and time periods, helping teams track issue resolution and project progress.

## Features

- **JIRA Integration**: Connects to JIRA data via the `jira-mcp-snowflake` MCP server
- **Automated Reporting**: Generates reports of closed issues from the last week
- **Multi-Project Support**: Can query multiple JIRA projects in a single report
- **Structured Output**: Presents results in clear, readable table format
- **Configurable**: Easy to modify for different projects, time ranges, and criteria

## Getting Started

Follow these steps to get your JIRA report agent up and running.

### Prerequisites

Before you begin, ensure you have the following:

- Python 3.9+ 
- pip (Python package installer)
- Access to a Llama Stack server
- The `jira-mcp-snowflake` MCP server configured locally

### Configuration

The agent is configured via `config.yaml`. The current configuration is set to report on:
- **Projects**: CCITJEN, CCITRP, QEHS
- **Time Range**: Last 7 days
- **Status**: Closed issues (status "6")

### Environment Variables

Set the following environment variables:

```bash
export REMOTE_BASE_URL="http://your-llama-stack-server:port"
export REMOTE_JIRA_MCP_URL="http://your-jira-mcp-server:port" # Optional if running locally
```

## Usage

### Running the JIRA Report Agent

To run the agent:
```bash
python src/agent.py
```

The agent will:
1. Connect to the Llama Stack server
2. Register the JIRA MCP tool group
3. Execute the configured prompts to generate JIRA reports
4. Output detailed information about closed issues

### Customizing Reports

1. **Change Projects**: Modify the project list in `config.yaml` under `user_prompts`
2. **Adjust Time Range**: Update the prompt to specify different time periods
3. **Filter Criteria**: Modify the status codes or add additional filters (priority, component, etc.)
4. **Output Format**: Customize the system prompt to change report formatting

### Example Output

The agent generates reports showing:
- Issue Key (e.g., CCITJEN-1234)
- Issue Summary/Title
- Priority Level
- Resolution Date
- Additional metadata as configured

## Contributing

Contributions are welcome! To improve this agent:

1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test with your JIRA data
5. Commit your changes:
   ```bash
   git commit -m 'Add new reporting feature'
   ```
6. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
