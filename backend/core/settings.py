from pydantic_settings import BaseSettings, SettingsConfigDict, root_validator
from sqlalchemy.engine import URL

class Settings(BaseSettings, case_sensitive=True):
    host: str = 'localhost'
    port: str = '5432'
    user: str
    password: str
    db_name: str
    driver: str = 'postgresql+asyncpg'

    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_pre_ping: bool = True

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        env_prefix='PG_',
        extra='ignore',
    )

    def url(self) -> str:
        # безопаснее, чем руками собирать строку
        return str(URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name,
        ))

    @root_validator(pre=True)
    def check_required_fields(cls, values):
        requierd_fields = [
            field for field, field_info in cls.__annotations__.items() if not values.get(field)
        ]

        for field in requierd_fields:
            if not values.get(field):
                raise ValueError(f'{field} требуется заполнение обязательного поля!')