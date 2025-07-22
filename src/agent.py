import logging
from llama_stack_client import LlamaStackClient
from llama_stack_client import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
import time
import uuid
import os
from .utils import step_logger
from .config import load_config
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# Get a logger instance
logger = logging.getLogger(__name__)

logger.info("Starting the JIRA report agent setup...")

config_file = os.getenv("CONFIG_FILE", "config.yaml")

# Load configuration
config = load_config(config_file)

base_url = os.getenv("REMOTE_BASE_URL")

# model_id will later be used to pass the name of the desired inference model to Llama Stack Agents/Inference APIs
model_id = "granite32-8b"

# Optional: Enter your MCP server URL here
jira_mcp_url = os.getenv("REMOTE_JIRA_MCP_URL")  # Local JIRA MCP server


def get_sampling_params():
    temperature = float(os.getenv("TEMPERATURE", 0.0))
    if temperature > 0.0:
        top_p = float(os.getenv("TOP_P", 0.95))
        strategy = {"type": "top_p", "temperature": temperature, "top_p": top_p}
    else:
        strategy = {"type": "greedy"}

    max_tokens = int(os.getenv("MAX_TOKENS", 2048))

    # sampling_params will later be used to pass the parameters to Llama Stack Agents/Inference APIs
    sampling_params = {
        "strategy": strategy,
        "max_tokens": max_tokens,
    }

    return sampling_params


sampling_params = get_sampling_params()
logger.info(
    f"Inference Parameters:\tModel: {model_id}\tSampling Parameters: {sampling_params}"
)


def create_client() -> LlamaStackClient:
    """
    Create a LlamaStackClient instance and register the JIRA MCP tool group.
    This function checks if the required tool groups are already registered,
    and if not, registers them with the Llama Stack server.
    Returns:
        LlamaStackClient: An instance of the LlamaStackClient connected to the specified base URL.
    """
    client = LlamaStackClient(
        base_url=base_url,
    )
    # Get list of registered tools and extract their toolgroup IDs
    registered_tools = client.tools.list()
    registered_toolgroups = [tool.toolgroup_id for tool in registered_tools]

    # Register JIRA MCP server if not already registered
    if "mcp::jira-mcp-snowflake" not in registered_toolgroups:
        logger.info("Registering JIRA MCP server...")
        client.toolgroups.register(
            toolgroup_id="mcp::jira-mcp-snowflake",
            provider_id="model-context-protocol",
            mcp_endpoint={"uri": jira_mcp_url} if jira_mcp_url else None,
        )

    # Log the current toolgroups registered
    logger.info(
        f"Your Llama Stack server is registered with the following tool groups: {set(registered_toolgroups)}\n"
    )
    return client


def create_agent(client: LlamaStackClient) -> Agent:
    """
    Create an agent with the specified model and JIRA tools.
    Args:
        client (LlamaStackClient): An instance of the LlamaStackClient connected to the Llama Stack server.
    """
    # Create agent with JIRA tools
    agent = Agent(
        client,
        model=model_id,
        instructions=config.prompts.system_prompt,
        tools=[
            "mcp::jira-mcp-snowflake",
        ],
        tool_config={"tool_choice": "auto"},
        sampling_params=sampling_params,
    )
    return agent


def run_task(agent_instance: Agent, use_stream=False):
    """
    Triggers the agent to perform its JIRA reporting task.

    Args:
        agent_instance (Agent): The agent instance to use for monitoring.
        use_stream (bool): Whether to stream the agent's response in real-time.
    """

    logger.info(f"Triggering JIRA report agent at {time.ctime()}...")

    user_prompts = config.prompts.user_prompts
    session_id = agent_instance.create_session(
        session_name=f"jira_report_session_{int(time.time())}"
    )
    
    for i, prompt in enumerate(user_prompts):
        logger.info(f"Processing prompt {i+1}: {prompt[:100]}...")
        response = agent_instance.create_turn(
            messages=[{"role": "user", "content": prompt}],
            session_id=session_id,
            stream=use_stream,
        )
        step_logger(response.steps)

    logger.info("JIRA report agent cycle completed.")


if __name__ == "__main__":
    client = create_client()
    agent = create_agent(client)
    
    try:
        run_task(agent)
    except Exception as e:
        logger.error(f"An error occurred during agent execution: {e}")
        raise
