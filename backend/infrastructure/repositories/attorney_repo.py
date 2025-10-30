from sqlalchemy.orm import Session
from sqlmodel import Session, select
from typing import List, TYPE_CHECKING
from backend.domain.entities.attorney import Attorney
from core.exceptions import EntityNotFoundException, DatabaseErrorException

from ..repositories.interfaces import IAttorneyRepository

if TYPE_CHECKING:
    from backend.domain.entities.attorney import Attorney


class AttorneyRepository(IAttorneyRepository):
    def __init__(self, session: Session):
        self.session = session

    # Целесообразность наличия данного метода пока не подтверждена
    def get(self, id: int) -> 'Attorney':
        '''Получить адвоката по ID.'''
        try:
            statement = select(Attorney).where(Attorney.id == id)
            attorney = self.session.exec(statement).first()
            if not attorney:
                raise EntityNotFoundException(
                    'Юрист'
                )  # Выбрасываем исключение, если не найдено
            else:
                return Attorney
        except Exception as e:
            raise DatabaseErrorException(
                f'Ошибка при получении юристов: {str(e)}'
            )  # Логируем или обрабатываем ошибки базы данных

    # Целесообразность наличия данного метода пока не подтверждена
    def get_all(self) -> List['Attorney']:
        try:
            statement = select(Attorney)
            attorneys = self.session.exec(statement).all()
            if not attorneys:
                raise EntityNotFoundException(
                    'Юрист'
                )  # Выбрасываем исключение, если не найдено
        except Exception as e:
            raise DatabaseErrorException(
                f'Ошибка при получении списка юристов: {str(e)}'
            )  # Логируем или обрабатываем ошибки базы данных

    def update(self) -> 'Attorney':
        try:
            statement = select(Attorney).where(Attorney.id == id)
            attorney = self.session.exec(statement).first()
            if not attorney:
                raise EntityNotFoundException(
                    'Юрист'
                )  # Выбрасываем исключение, если не найдено
            else:
                pass
        except Exception as e:
            raise DatabaseErrorException(
                f'Ошибка при получении юристов: {str(e)}'
            )  # Логируем или обрабатываем ошибки базы данных

    def delete(self) -> 'Attorney':
        pass
