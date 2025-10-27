from pydantic_settings import BaseSettings, SettingsConfigDict, root_validator
from sqlalchemy.engine import URL

class Settings(BaseSettings):
    '''Конфигурация приложения (читается из .env файла).'''

    # Параметры БД
    host: str = 'localhost'
    port: int = 5432
    user: str
    password: str
    db_name: str

    # SQLAlchemy параметры
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
        case_sensitive=True,
    )

    def url(self) -> str:
        '''Собрать URL подключения безопасно (защита от SQL injection).'''
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