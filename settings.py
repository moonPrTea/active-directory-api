from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LDAPSettings(BaseSettings):
    HOST: str = "<host>"
    PORT: int = 636
    BASE_DN: str = "<base_db>"
    USERNAME: str = "<username>"
    PASSWORD: SecretStr
    USER_OU: str = "Users"
    GROUP_OU: str = "Groups"

    USE_SSL: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LDAP_",
        extra="ignore",
    )

    @property
    def server_url(self) -> str:
        protocol = "ldaps" if self.USE_SSL else "ldap"
        return f"{protocol}://{self.HOST}:{self.PORT}"


class LogSettings(BaseSettings):
    DIR: str = "<directory>"
    LEVEL: str = "<info>"
    ROTATION: str = "<rotation>"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LOG_",
        extra="ignore",
    )


class TokenSettings(BaseSettings):
    AUTH_TOKEN: SecretStr
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LDAP_",
        extra="ignore",
    )


class Settings(BaseSettings):
    ldap: LDAPSettings = LDAPSettings()
    log: LogSettings = LogSettings()
    token: TokenSettings = TokenSettings()


settings = Settings()
