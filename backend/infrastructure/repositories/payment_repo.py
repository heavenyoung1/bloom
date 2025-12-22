from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from backend.domain.entities.payment import ClientPayment
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.infrastructure.mappers.payment_mapper import ClientPaymentMapper
from typing import TYPE_CHECKING, List
from backend.infrastructure.models.payment import ClientPaymentORM

from backend.core.logger import logger

class PaymentRepository():

    def __init__(self, session):
        self.session = session

    async def save(self, payment: ClientPayment) -> 'ClientPayment':
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_payment = ClientPaymentMapper.to_orm(payment)

            # 2. Добавление в сессию
            self.session.add(orm_payment)
            
            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Обновляем ID в доменном объекте
            payment.id = orm_payment.id

            logger.info(f'Платеж сохранено. ID - {payment.id}')
            return payment

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении ДЕЛА: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении ДЕЛА: {str(e)}')

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении ДЕЛА: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении ДЕЛА: {str(e)}')
        
    async def get(self, id: int) -> 'ClientPayment':
        try:
            # 1. Получение записи из базы данных
            stmt = select(ClientPaymentORM).where(ClientPaymentORM.id == id)
            result = await self.session.execute(stmt)
            orm_payment = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_payment:
                return None
                # raise EntityNotFoundException(f'Дело с ID {id} не найдено')

            # 3. Преобразование ORM объекта в доменную сущность
            payment = ClientPaymentMapper.to_domain(orm_payment)

            logger.info(f'ПЛАТЕЖ получен. ID - {payment.id}')
            return payment

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении платежа ID = {id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении платежа: {str(e)}')


    async def get_all_for_attorney(self, id: int) -> List['ClientPayment']:
        try:
            # 1. Получение записей из базы данных
            stmt = (
                select(ClientPaymentORM)
                .where(ClientPaymentORM.attorney_id == id)  # Фильтрация по адвокату
                .order_by(ClientPaymentORM.created_at.desc())  # Например, сортировка по дате
            )
            result = await self.session.execute(stmt)
            orm_payments = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [ClientPaymentMapper.to_domain(orm_payment) for orm_payment in orm_payments]

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении всех ПЛАТЕЖЕЙ: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при получении ПЛАТЕЖЕЙ: {str(e)}')

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(ClientPaymentORM).where(ClientPaymentORM.id == id)
            result = await self.session.execute(stmt)
            orm_payment = result.scalars().first()

            if not orm_payment:
                logger.warning(f'ПЛАТЕЖ с ID {id} не найден при удалении.')
                raise EntityNotFoundException(f'ПЛАТЕЖ с ID {id} не найдено')

            # 2. Удаление
            await self.session.delete(orm_payment)
            await self.session.flush()

            logger.info(f'ПЛАТЕЖ с ID {id} успешно удалено.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении ПЛАТЕЖ: {str(e)}')

