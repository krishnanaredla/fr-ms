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
    SNS_TARGET_ARN : str = None
    

    class Config:
        """
        Loads the .env file
        """

        env_file: str = ".env"


class TestConfig(GlobalConfig):
    """"""

    class Config:
        env_prefix: str = "TEST_"


class DevConfig(GlobalConfig):
    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    class Config:
        env_prefix: str = "PROD_"


class RunConfig:
    def __init__(self, env_state: Optional[str], env_loc: Optional[str] = ".env"):
        self.env_state = env_state
        self.env_loc = env_loc

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig(_env_file=self.env_loc)
        if self.env_state == "test":
            return TestConfig(_env_file=self.env_loc)
        if self.env_state == "prod":
            return ProdConfig(_env_file=self.env_loc)


def getConfig(env_loc: Optional[str] = "config/.env") -> BaseSettings:
    if os.environ.get("envPath", None):
        envPath = os.environ.get("envPath")
    else:
        envPath = Path.cwd().joinpath(env_loc)
    return RunConfig(GlobalConfig(_env_file=env_loc).ENV_STATE, envPath)()
