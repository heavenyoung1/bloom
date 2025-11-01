from typing import Dict, List, TYPE_CHECKING
from sqlmodel import select
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.domain.entities.attorney import Attorney
from backend.infrastructure.mappers import AttorneyMapper
from backend.infrastructure.models import AttorneyORM
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from ..repositories.interfaces import IAttorneyRepository

if TYPE_CHECKING:
    from backend.domain.entities.attorney import Attorney


class AttorneyRepository(IAttorneyRepository):
    '''
    Репозиторий для работы с данными юристов в базе данных.

    Реализует интерфейс IAttorneyRepository и предоставляет методы для сохранения,
    обновления, удаления и получения юристов из базы данных.
    '''
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, attorney: Attorney) -> Dict:
        '''
        Сохранить нового юриста в базе данных.

        Проверяет, существует ли уже юрист с данным ID. Если нет, добавляет нового.

        :param attorney: Объект юриста, который нужно сохранить.
        :return: Словарь с ключами 'success' (True, если сохранение успешно) и 'id' (ID сохранённого юриста).
        '''
        try:
            statement = select(AttorneyORM).where(AttorneyORM.id == attorney.id)
            result = await self.session.exec(statement)
            attorney_searched = result.first()

            if attorney_searched is None:  # Если юрист не найден, добавляем нового
                orm_attorney = AttorneyMapper.to_orm(domain=attorney)
                self.session.add(orm_attorney)
                await self.session.flush()  # ⚠️ фиксируем INSERT в транзакции
                return {'success': True, 'id': orm_attorney.id}
            else:
                return {'success': False, 'id': attorney_searched.id}
        except IntegrityError as e:
            # Ловим ошибку попытки сохранения неуникальных данных
            if 'attorneys_attorney_id_key' in str(e):
                return {'success': False, 'id': None}
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при сохранении юриста: {str(e)}')

    async def get(self, id: int) -> 'Attorney':
        '''
        Получить юриста по ID.

        :param id: ID юриста.
        :return: Объект юриста, если найден.
        :raises DatabaseErrorException: Если произошла ошибка при получении юриста.
        '''
        try:
            statement = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.exec(statement)
            orm_attorney = result.first()

            if not orm_attorney:
                return None

            attorney = AttorneyMapper.to_domain(orm_attorney)
            return attorney
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении юриста: {str(e)}')

    async def get_by_attorney_id(self, attorney_id: str) -> 'Attorney':
        '''
        Получить юриста по его уникальному номеру удостоверения (attorney_id).

        :param attorney_id: Уникальный ID юриста.
        :return: Объект юриста, если найден.
        :raises DatabaseErrorException: Если произошла ошибка при получении юриста.
        '''
        try:
            statement = select(AttorneyORM).where(
                AttorneyORM.attorney_id == attorney_id
            )
            result = await self.session.exec(statement)
            orm_attorney = result.first()
            attorney = AttorneyMapper.to_domain(orm_attorney)

            if not attorney:
                return None

            return attorney
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении юриста: {str(e)}')

    async def get_all(self) -> List['Attorney']:
        '''
        Получить всех юристов из базы данных.

        :return: Список всех юристов в базе данных.
        :raises DatabaseErrorException: Если произошла ошибка при получении списка юристов.
        '''
        try:
            statement = select(AttorneyORM)
            result = await self.session.exec(statement)
            orm_attorneys = result.all()
            if not orm_attorneys:
                raise EntityNotFoundException('Юристы не найдены')

            domain_attorneys = [
                AttorneyMapper.to_domain(orm_attorney) for orm_attorney in orm_attorneys
            ]
            return domain_attorneys
        except Exception as e:
            raise DatabaseErrorException(
                f'Ошибка при получении списка юристов: {str(e)}'
            )

    async def update(self, id: int, updated_attorney: Attorney) -> Dict:
        '''
        Обновить данные юриста по ID.

        :param id: ID юриста, который необходимо обновить.
        :param updated_attorney: Обновленные данные юриста.
        :return: Словарь с результатом операции ('success': True) и обновлённым юристом.
        :raises DatabaseErrorException: Если произошла ошибка при обновлении данных.
        '''
        try:
            statement = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.exec(statement)
            orm_attorney = result.first()

            if not orm_attorney:
                raise EntityNotFoundException('Юрист не найден')
            attorney = AttorneyMapper.to_domain(orm_attorney)

            # Обновляем поля адвоката
            attorney.first_name = updated_attorney.first_name
            attorney.last_name = updated_attorney.last_name
            attorney.patronymic = updated_attorney.patronymic
            attorney.email = updated_attorney.email
            attorney.phone = updated_attorney.phone
            attorney.password_hash = updated_attorney.password_hash
            attorney.updated_at = func.now()

            # Преобразуем обновленного адвоката обратно в ORM модель
            updated_orm_attorney = AttorneyMapper.to_orm(attorney)

            # Важно: update здесь сохраняет изменения без явного merge и flush
            return {'success': True, 'attorney': attorney}
        except Exception as e:
            raise DatabaseErrorException(
                f'Ошибка при обновлении данных юриста: {str(e)}'
            )

    async def delete(self, id: int) -> bool:
        '''
        Удалить юриста по ID.

        :param id: ID юриста, которого нужно удалить.
        :return: True, если удаление прошло успешно.
        :raises DatabaseErrorException: Если произошла ошибка при удалении.
        '''
        try:
            statement = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.exec(statement)
            orm_attorney = result.first()

            if not orm_attorney:
                raise EntityNotFoundException('Юрист не найден')

            await self.session.delete(orm_attorney)
            await self.session.flush()  # Фиксируем изменения в транзакции
            return True 
        
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при удалении юриста: {str(e)}')
