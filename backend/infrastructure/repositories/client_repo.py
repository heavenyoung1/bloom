from typing import TYPE_CHECKING, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logger import logger
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.domain.entities.client import Client
from backend.infrastructure.mappers import ClientMapper
from backend.infrastructure.models import ClientORM, CaseORM
from backend.application.interfaces.repositories.client_repo import IClientRepository

if TYPE_CHECKING:
    from backend.domain.entities.client import Client


class ClientRepository(IClientRepository):
    '''
    Репозиторий для работы с сущностью «Клиент» (Client) в базе данных.
    Реализует асинхронные CRUD-операции через SQLAlchemy 2.0+.
    '''

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, client: Client) -> 'Client':
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_client = ClientMapper.to_orm(client)

            # 2. Добавление в сессию
            self.session.add(orm_client)

            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Обновляем ID в доменном объекте
            client.id = orm_client.id

            logger.info(f'КЛИЕНТ сохранен. ID - {client.id}')
            return client

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении КЛИЕНТА: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении КЛИЕНТА: {str(e)}')

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении КЛИЕНТА: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении КЛИЕНТА: {str(e)}')

    async def get(self, id: int) -> 'Client':
        try:
            # 1. Получение записи из базы данных
            stmt = select(ClientORM).where(ClientORM.id == id)
            result = await self.session.execute(stmt)
            orm_client = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_client:
                return None

            # 3. Преобразование ORM объекта в доменную сущность
            client = ClientMapper.to_domain(orm_client)

            logger.info(f'КЛИЕНТ получен. ID - {client.id}')
            return client

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении КЛИЕНТА ID={id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении КЛИЕНТА: {str(e)}')

    async def get_all_for_attorney(self, id: int) -> List['Client']:
        try:
            # 1. Получение записей из базы данных
            stmt = (
                select(ClientORM)
                .where(ClientORM.owner_attorney_id == id)  # Фильтрация по адвокату
                .order_by(ClientORM.created_at.desc())  # Например, сортировка по дате
            )
            result = await self.session.execute(stmt)
            orm_clients = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [ClientMapper.to_domain(orm_client) for orm_client in orm_clients]

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении КЛИЕНТА ID={id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении КЛИЕНТА: {str(e)}')

    async def get_for_case(self, case_id: int) -> List['Client']:
        try:
            # 1. Получение клиента через связь с делом
            stmt = (
                select(ClientORM)
                .join(CaseORM, ClientORM.id == CaseORM.client_id)
                .where(CaseORM.id == case_id)  # Фильтрация по делу
            )
            result = await self.session.execute(stmt)
            orm_clients = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [ClientMapper.to_domain(orm_client) for orm_client in orm_clients]

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении КЛИЕНТА для дела ID={case_id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении КЛИЕНТА для дела: {str(e)}')

    async def update(self, updated_client: Client) -> 'Client':
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(ClientORM).where(ClientORM.id == updated_client.id)
            result = await self.session.execute(stmt)
            orm_client = result.scalars().first()

            # 2. Проверка наличия записи в БД
            if not orm_client:
                logger.error(f'КЛИЕНТ с ID {updated_client.id} не найден.')
                raise EntityNotFoundException(
                    f'КЛИЕНТ с ID {updated_client.id} не найден.'
                )

            # 3. Обновление полей ORM-объекта из доменной сущности
            ClientMapper.update_orm(orm_client, updated_client)

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'КЛИЕНТ обновлен. ID= {updated_client.id}')
            return ClientMapper.to_domain(orm_client)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при обновлении КЛИЕНТА. ID={updated_client.id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка БД при обновлении КЛИЕНТА. ID={updated_client.id}: {e}'
            )

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(ClientORM).where(ClientORM.id == id)
            result = await self.session.execute(stmt)
            orm_client = result.scalars().first()

            if not orm_client:
                logger.warning(f'КЛИЕНТ с ID {id} не найден при удалении.')
                raise EntityNotFoundException(
                    f'КЛИЕНТ с ID {id} не найден при удалении.'
                )

            # 2. Удаление
            await self.session.delete(orm_client)
            await self.session.flush()

            logger.info(f'КЛИЕНТ с ID {id} успешно удален.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении КЛИЕНТА: {str(e)}')

    async def get_by_email_for_owner(self, email: str, owner_id: int) -> 'Client':
        '''Получить клиента по email для конкретного адвоката.'''
        return await self._get_by_field_for_owner(
            ClientORM.email == email, 'email', email, owner_id
        )

    async def get_by_phone_for_owner(self, phone: str, owner_id: int) -> 'Client':
        '''Получить клиента по телефону для конкретного адвоката.'''
        return await self._get_by_field_for_owner(
            ClientORM.phone == phone, 'phone', phone, owner_id
        )

    async def get_by_personal_info_for_owner(
        self, personal_info: str, owner_id: int
    ) -> 'Client':
        '''Получить клиента по персональным данным для конкретного адвоката.'''
        return await self._get_by_field_for_owner(
            ClientORM.personal_info == personal_info,
            'personal_info',
            personal_info,
            owner_id,
        )

    async def _get_by_field_for_owner(
        self, condition, field_name: str, field_value: str, owner_id: int
    ) -> 'Client':
        '''
        Вспомогательный метод для получения клиента по произвольному полю для конкретного адвоката.
        
        Args:
            condition: SQLAlchemy условие для фильтрации
            field_name: Название поля для логирования
            field_value: Значение поля для логирования
            owner_id: ID адвоката-владельца
            
        Returns:
            Client | None: Найденный клиент или None
        '''
        try:
            stmt = select(ClientORM).where(
                condition, ClientORM.owner_attorney_id == owner_id
            )
            result = await self.session.execute(stmt)
            orm_client = result.scalars().first()

            if not orm_client:
                return None

            client = ClientMapper.to_domain(orm_client)
            logger.info(
                f'КЛИЕНТ успешно получен по {field_name} для адвоката {owner_id}. ID - {client.id}. {field_name} - {field_value}.'
            )
            return client

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении КЛИЕНТА по {field_name}={field_value} для адвоката {owner_id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка БД при получении КЛИЕНТА по {field_name}: {str(e)}'
            )
