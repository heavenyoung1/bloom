from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings, case_sensitive=True):
    host: str = 'localhost'
    port: str = '5432'
    user: str
    password: str
    db_name: str

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        env_prefix='PG_',
        extra='ignore',
    )

    def get_db_url(self):
        return(
            f'postgresql+asyncpg://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.db_name}'
            )

