import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()
class LDAPSettings(BaseSettings):
    ADRESS: str = 'localhost'
    PORT: int = 636
    BASE_DC: str = 'dc=example,dc=ru'
    USERNAME: str = 'user'
    PASSWORD: str = 'password'
    USER_OU: str = 'user'
    GROUP_OU: str = 'group'
    model_config = SettingsConfigDict(env_file='.env', extra="allow")

ldap_settings = LDAPSettings()  

class LogSettings(BaseSettings):
    LOG_DIR: str = 'log_dir'
    LEVEL: str = 'level'
    ROTATION: str = 'rotation'
    model_config = SettingsConfigDict(env_file='.env', extra="allow")

log_settings = LogSettings()

class BotSettings(BaseSettings):
    TOKEN: str = 'token'
    USER_ID: str = 'user_id'

bot_settings = BotSettings()

class TokenSettings(BaseSettings):
    AUTH_TOKEN: str = 'token'
    model_config = SettingsConfigDict(env_file='.env', extra="allow")

token_settings = TokenSettings()