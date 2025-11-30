from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    '''
    Базовый класс для всех ORM моделей.
    
    ⚠️ НЕ должен содержать:
    - id (это добавляет SQLAlchemyBaseUserTable или конкретная модель)
    - Любые другие поля
    
    Только метаданные и общие методы (если нужны).
    '''
    pass
