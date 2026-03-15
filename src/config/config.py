from dishka import provide, Provider, Scope
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    version: str = '1.0.0'
    service: str = 'currency'
    port: int = 8000
    author: str = 'p.zenchenkov'

    model_config = SettingsConfigDict(env_file='.env')


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def create_settings(self) -> Settings:
        return Settings()
