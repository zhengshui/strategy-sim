"""
Configuration settings for StrategySim AI.

Uses pydantic-settings for environment variable management and validation.
"""

import os
from typing import Optional, Literal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Model Configuration
    openai_api_key: str = Field(..., description="OpenAI API key for AutoGen agents")
    model_provider: Literal["openai", "anthropic", "azure"] = Field(
        default="openai", description="LLM provider to use"
    )
    model_name: str = Field(default="gpt-4o", description="Model name to use")

    # Application Settings
    debug: bool = Field(default=False, description="Debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="Logging level"
    )

    # Chainlit Configuration
    chainlit_auth_secret: Optional[str] = Field(
        default=None, description="Secret key for Chainlit authentication"
    )
    chainlit_host: str = Field(default="0.0.0.0", description="Host for Chainlit app")
    chainlit_port: int = Field(default=8000, description="Port for Chainlit app")

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./strategysim.db",
        description="Database URL for session persistence",
    )

    # Optional External APIs
    market_data_api_key: Optional[str] = Field(
        default=None, description="API key for market data services"
    )
    legal_database_api_key: Optional[str] = Field(
        default=None, description="API key for legal database services"
    )

    # Analytics and Monitoring
    analytics_enabled: bool = Field(
        default=False, description="Enable analytics tracking"
    )
    analytics_api_key: Optional[str] = Field(
        default=None, description="API key for analytics service"
    )

    # Email Configuration
    smtp_host: Optional[str] = Field(default=None, description="SMTP server host")
    smtp_port: int = Field(default=587, description="SMTP server port")
    smtp_user: Optional[str] = Field(default=None, description="SMTP username")
    smtp_password: Optional[str] = Field(default=None, description="SMTP password")

    # Agent Configuration
    max_agent_turns: int = Field(
        default=20, description="Maximum turns for agent conversations"
    )
    agent_timeout: int = Field(
        default=300, description="Timeout for agent responses in seconds"
    )

    # Decision Analysis Configuration
    monte_carlo_iterations: int = Field(
        default=1000, description="Number of Monte Carlo simulation iterations"
    )
    risk_threshold: float = Field(
        default=0.7, description="Risk threshold for decision analysis"
    )

    @field_validator("openai_api_key")
    def validate_openai_key(cls, v: str) -> str:
        """Validate OpenAI API key format."""
        if not v.startswith("sk-"):
            raise ValueError("OpenAI API key must start with 'sk-'")
        return v

    @field_validator("chainlit_port")
    def validate_port(cls, v: int) -> int:
        """Validate port number range."""
        if not (1024 <= v <= 65535):
            raise ValueError("Port must be between 1024 and 65535")
        return v

    @field_validator("risk_threshold")
    def validate_risk_threshold(cls, v: float) -> float:
        """Validate risk threshold range."""
        if not (0.0 <= v <= 1.0):
            raise ValueError("Risk threshold must be between 0.0 and 1.0")
        return v

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_model_config() -> dict:
    """Get model configuration for AutoGen."""
    provider_map = {
        "openai": "autogen_ext.models.openai.OpenAIChatCompletionClient",
        "azure": "autogen_ext.models.openai.AzureOpenAIChatCompletionClient",
        "anthropic": "autogen_ext.models.anthropic.AnthropicChatCompletionClient"
    }
    
    return {
        "provider": provider_map.get(settings.model_provider, provider_map["openai"]),
        "config": {
            "model": settings.model_name,
            "api_key": settings.openai_api_key,
        },
    }


def validate_settings() -> None:
    """Validate all required settings are present."""
    try:
        # This will raise validation errors if any required fields are missing
        Settings()
    except Exception as e:
        raise RuntimeError(f"Invalid configuration: {e}") from e


# Validate settings on import
if __name__ != "__main__":
    validate_settings()