import logging
import yaml
from typing import List
from pydantic import BaseModel, Field, field_validator


logger = logging.getLogger(__name__)


# Pydantic models for configuration
class RAGUrl(BaseModel):
    """Model for individual RAG URL configuration"""

    url: str = Field(..., description="URL of the document to ingest")
    mime_type: str = Field(..., description="MIME type of the document")

    @field_validator("url")
    def validate_url(cls, v):
        if not v.strip():
            raise ValueError("URL cannot be empty")
        return v.strip()

    @field_validator("mime_type")
    def validate_mime_type(cls, v):
        allowed_types = [
            "application/pdf",
            "text/plain",
            "text/html",
            "application/json",
        ]
        if v not in allowed_types:
            logger.warning(
                f"MIME type '{v}' may not be supported. Allowed types: {allowed_types}"
            )
        return v


class RAGConfig(BaseModel):
    """Model for RAG configuration section"""

    urls: List[RAGUrl] = Field(
        ..., description="List of URLs to ingest into RAG system"
    )



class PromptsConfig(BaseModel):
    """Model for prompts configuration section"""

    system_prompt: str = Field(..., description="System prompt for the agent")
    user_prompts: List[str] = Field(..., description="List of user prompts to execute")

    @field_validator("system_prompt")
    def validate_system_prompt(cls, v):
        if not v.strip():
            raise ValueError("System prompt cannot be empty")
        return v.strip()

    @field_validator("user_prompts")
    def validate_user_prompts(cls, v):
        if not v:
            raise ValueError("At least one user prompt must be provided")
        return [prompt.strip() for prompt in v if prompt.strip()]


class Config(BaseModel):
    """Main configuration model"""

    rag: RAGConfig = Field(..., description="RAG system configuration")
    prompts: PromptsConfig = Field(..., description="Prompts configuration")


def load_config(config_path: str = "config.yaml") -> Config:
    """
    Load configuration from YAML file and validate using Pydantic models.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        Config: Validated configuration object.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)
        logger.info(f"Configuration loaded from {config_path}")

        # Validate and create Pydantic model
        config = Config(**config_data)
        logger.info("Configuration validated successfully")
        logger.info(
            f"Loaded {len(config.rag.urls)} RAG URL(s) and {len(config.prompts.user_prompts)} user prompt(s)"
        )

        return config
    except FileNotFoundError:
        logger.error(f"Configuration file {config_path} not found")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {config_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error validating configuration: {e}")
        raise
