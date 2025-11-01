from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict, List, TYPE_CHECKING
from backend.domain.entities.attorney import Attorney
from backend.infrastructure.mappers import AttorneyMapper
from backend.infrastructure.models import AttorneyORM
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException

from ..repositories.interfaces import IAttorneyRepository

if TYPE_CHECKING:
    from backend.domain.entities.attorney import Attorney


class AttorneyRepository(IAttorneyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, attorney: Attorney) -> Dict:
        '''
        Сохранить юриста в БД.
        Возвращает:
            {'success': True, 'id': int}  — если запись добавлена
            {'success': False, 'id': None} — если дубликат
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

    # Целесообразность наличия данного метода пока не подтверждена
    async def get(self, id: int) -> 'Attorney':
        '''Получить адвоката по ID.'''
        try:
            statement = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.exec(statement)
            attorney = result.first()

            if not attorney:
                return None
                # raise EntityNotFoundException('Юрист не найден')

            return attorney
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении юриста: {str(e)}')

    async def get_by_attorney_id(self, attorney_id: str) -> 'Attorney':
        '''Получить адвоката по ID.'''
        try:
            statement = select(AttorneyORM).where(
                AttorneyORM.attorney_id == attorney_id
            )
            result = await self.session.exec(statement)
            orm_attorney = result.first()
            attorney = AttorneyMapper.to_domain(orm_attorney)

            if not attorney:
                return None
                # raise EntityNotFoundException('Юрист не найден')

            return attorney
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении юриста: {str(e)}')

    # Целесообразность наличия данного метода пока не подтверждена
    async def get_all(self) -> List['Attorney']:
        '''Получить всех юристовю.'''
        try:
            statement = select(AttorneyORM)
            result = await self.session.exec(statement)
            orm_attorneys = result.all()
            domain_attorneys = [
                AttorneyMapper.to_domain(orm_attorney) for orm_attorney in orm_attorneys
            ]

            if not domain_attorneys:
                raise EntityNotFoundException('Юристы не найдены')

            return domain_attorneys
        except Exception as e:
            raise DatabaseErrorException(
                f'Ошибка при получении списка юристов: {str(e)}'
            )

    async def update(self, id: int, updated_attorney: Attorney) -> Dict:
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
            attorney.is_active = updated_attorney.is_active
            # attorney.updated_at = updated_attorney.updated_at

            # Преобразуем обновленного адвоката обратно в ORM модель
            updated_orm_attorney = AttorneyMapper.to_orm(attorney)

            # ПОЧЕМУ ЭТО РАБОТАЕТ БЕЗ MERGE и FLUSH???
            # await self.session.flush()  # ⚠️ фиксируем INSERT в транзакции
            # await self.session.merge(updated_orm_attorney)

            return {'success': True, 'attorney': attorney}
        except Exception as e:
            raise DatabaseErrorException(
                f'Ошибка при обновлении данных юриста: {str(e)}'
            )

    async def delete(self, id: int) -> bool:
        '''Удалить юриста по ID'''
        try:
            statement = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.exec(statement)
            orm_attorney = result.first()

            if not orm_attorney:
                raise EntityNotFoundException('Юрист не найден')
                # Удаляем адвоката

            await self.session.delete(orm_attorney)
            await self.session.flush()  # ⚠️ фиксируем INSERT в транзакции
            return True  # Возвращаем True, если удаление прошло успешно
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при удалении юриста: {str(e)}')
