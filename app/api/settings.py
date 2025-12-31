from typing import List, Optional
from pydantic import BaseSettings, Field, BaseModel
import os
from pathlib import Path


class AppConfig(BaseModel):
    """
    Application related configuration
    """

    prefix: str = "/api/v1/fileregister"
    tags: List[str] = ["fileregister"]


class GlobalConfig(BaseSettings):
    """
    Global configurations.
    These variables will be loaded from the .env file. However, if
    there is a shell environment variable having the same name,
    that will take precedence.
    """

    APP_CONFIG: AppConfig = AppConfig()

    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")

    DB_USER: str = None
    DB_PASS: str = None
    DB_HOST: str = None
    DB_PORT: str = None
    DB_DATABASE: str = None
    SNS_TARGET_ARN: str = None
    SNS_ENDPOINT_URL: str = "http://localhost:4566"
    SNS_REGION_NAME: str = "us-east-1"
    

    class Config:
        """
        Loads the .env file
        """

        env_file: str = ".env"


class TestConfig(GlobalConfig):
    """Test environment configuration with TEST_ prefix."""

    class Config:
        env_prefix: str = "TEST_"


class DevConfig(GlobalConfig):
    """Development environment configuration with DEV_ prefix."""
    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    """Production environment configuration with PROD_ prefix."""
    class Config:
        env_prefix: str = "PROD_"


class RunConfig:
    """
    Configuration factory that returns the appropriate config based on environment state.
    """
    def __init__(self, env_state: Optional[str], env_loc: Optional[str] = ".env"):
        self.env_state = env_state
        self.env_loc = env_loc

    def __call__(self):
        """
        Returns the appropriate configuration instance based on environment state.
        
        Returns:
            Configuration instance (DevConfig, TestConfig, or ProdConfig)
        """
        if self.env_state == "dev":
            return DevConfig(_env_file=self.env_loc)
        if self.env_state == "test":
            return TestConfig(_env_file=self.env_loc)
        if self.env_state == "prod":
            return ProdConfig(_env_file=self.env_loc)


def getConfig(env_loc: Optional[str] = "config/.env") -> BaseSettings:
    """
    Get the configuration instance based on the current environment.
    
    Args:
        env_loc: Path to the .env file (default: "config/.env")
        
    Returns:
        BaseSettings: Configuration instance for the current environment
    """
    if os.environ.get("envPath", None):
        envPath = os.environ.get("envPath")
    else:
        envPath = Path.cwd().joinpath(env_loc)
    return RunConfig(GlobalConfig(_env_file=env_loc).ENV_STATE, envPath)()
