import os
from typing import List
from pydantic import Field, SecretStr, PositiveInt, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    """
    Configuration settings loaded exclusively from environment variables.
    All fields are required as no default values are provided.
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # General Settings 
    debug: bool = Field(description="Enable debug mode.")
    project_name: str = Field(description="Name of the project.")
    project_version: str = Field(description="Version of the project.")

    # JWT Settings 
    jwt_algo: str = Field(description="Algorithm for JWT signing.")
    jwt_secret: SecretStr = Field(description="Secret key for JWT signing.") 
    jwt_expires_min: PositiveInt = Field(description="JWT expiration time in minutes.") 

    # OpenAI Settings 
    openai_key: SecretStr = Field(description="OpenAI API key.")
    
    # Whitelist URLs
    whitelist_ips: str = Field(description="Allowed origin URLs for CORS.")

config = Settings()
