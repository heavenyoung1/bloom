from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from backend.domain.entities.client_payment import ClientPayment
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.infrastructure.mappers.payment_mapper import ClientPaymentMapper
from typing import TYPE_CHECKING, List, Sequence
from backend.infrastructure.models.payment import ClientPaymentORM
from backend.application.interfaces.repositories.payment_repo import IPaymentRepository

from backend.core.logger import logger


class ClientPaymentRepository(IPaymentRepository):

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

    async def get_all_for_attorney(self, id: int) -> Sequence['ClientPayment']:
        try:
            # 1. Получение записей из базы данных
            stmt = (
                select(ClientPaymentORM)
                .where(ClientPaymentORM.attorney_id == id)  # Фильтрация по адвокату
                .order_by(
                    ClientPaymentORM.created_at.desc()
                )  # Например, сортировка по дате
            )
            result = await self.session.execute(stmt)
            orm_payments = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [
                ClientPaymentMapper.to_domain(orm_payment)
                for orm_payment in orm_payments
            ]

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении всех ПЛАТЕЖЕЙ: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при получении ПЛАТЕЖЕЙ: {str(e)}')

    async def update(self, updated_payment: ClientPayment) -> 'ClientPayment':
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(ClientPaymentORM).where(
                ClientPaymentORM.id == updated_payment.id
            )
            result = await self.session.execute(stmt)
            orm_payment = result.scalars().first()

            # 2. Проверка наличия записи в БД
            if not orm_payment:
                logger.error(f'Платеж с ID {updated_payment.id} не найден.')
                raise EntityNotFoundException(
                    f'Платеж с ID {updated_payment.id} не найден'
                )

            # 3. Прямое обновление полей ORM-объекта
            orm_payment.name = updated_payment.name
            orm_payment.client_id = updated_payment.client_id
            orm_payment.attorney_id = updated_payment.attorney_id
            orm_payment.paid = updated_payment.paid
            orm_payment.paid_str = updated_payment.paid_str
            orm_payment.pade_date = updated_payment.pade_date
            orm_payment.paid_deadline = updated_payment.paid_deadline
            orm_payment.status = updated_payment.status
            orm_payment.taxable = updated_payment.taxable
            orm_payment.condition = updated_payment.condition

            # 4. Сохранение в БД
            await self.session.flush()

            # 5. Возврат доменного объекта
            logger.info(f'Платеж обновлен. ID = {updated_payment.id}')
            return ClientPaymentMapper.to_domain(orm_payment)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при обновлении платежа ID = {updated_payment.id}: {e}'
            )
            raise DatabaseErrorException(f'Ошибка при обновлении платежа: {str(e)}')

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(ClientPaymentORM).where(ClientPaymentORM.id == id)
            result = await self.session.execute(stmt)
            orm_payment = result.scalars().first()

            if not orm_payment:
                logger.warning(f'Платеж с ID {id} не найден при удалении.')
                raise EntityNotFoundException(f'Платеж с ID {id} не найден')

            # 2. Удаление
            await self.session.delete(orm_payment)
            await self.session.flush()

            logger.info(f'Платеж с ID {id} успешно удален.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении платежа: {str(e)}')
