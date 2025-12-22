from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from backend.domain.entities.payment_detail import PaymentDetail
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.infrastructure.mappers.payment_detail_mapper import PaymentDetailMapper
from typing import TYPE_CHECKING, List
from backend.infrastructure.models.payment_detail import PaymentDetailORM

from backend.core.logger import logger


class PaymentDetailRepository():

    def __init__(self, session):
        self.session = session

    async def save(self, payment_detail: PaymentDetail) -> 'PaymentDetail':
        try:
            # 1. Конвертация доменной сущности в ORM-объект  
            orm_payment_detail = PaymentDetailMapper.to_orm(payment_detail)

            # 2. Добавление в сессию
            self.session.add(orm_payment_detail)
            
            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Обновляем ID в доменном объекте
            payment_detail.id = orm_payment_detail.id

            logger.info(f'Платежная информация успешно сохранена. ID - {payment_detail.id}')
            return payment_detail

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении платежной информации: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении платежной информации: {str(e)}')

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении платежной информации: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении платежной информации: {str(e)}')

    async def get(self, id: int) -> 'PaymentDetail':
        try:
            # 1. Получение записи из базы данных
            stmt = select(PaymentDetailORM).where(PaymentDetailORM.id == id)
            result = await self.session.execute(stmt)
            orm_payment_detail = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_payment_detail:
                return None
                # raise EntityNotFoundException(f'Дело с ID {id} не найдено')

            # 3. Преобразование ORM объекта в доменную сущность
            payment_detail = PaymentDetailMapper.to_domain(orm_payment_detail)

            logger.info(f'ПЛАТЕЖ получен. ID - {payment_detail.payment_detail_id}')
            return payment_detail

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении платежа ID = {id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении платежа: {str(e)}')
        
    async def update(self, updated_payment_detail: PaymentDetail) -> 'PaymentDetail':
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(PaymentDetailORM).where(
                PaymentDetailORM.id == updated_payment_detail.id
                )
            result = await self.session.execute(stmt)
            orm_payment_detail = result.scalars().first()

            # 2. Проверка наличия записи в БД
            if not orm_payment_detail:
                logger.error(f'Дело с ID {updated_payment_detail.id} не найдено.')
                raise EntityNotFoundException(f'Дело с ID {updated_payment_detail.id} не найдено')

            # 3. Прямое обновление полей ORM-объекта
            orm_payment_detail.inn = updated_payment_detail.inn
            orm_payment_detail.kpp = updated_payment_detail.kpp
            orm_payment_detail.index_address = updated_payment_detail.index_address
            orm_payment_detail.address = updated_payment_detail.address
            orm_payment_detail.bank_account = updated_payment_detail.inbank_accountn
            orm_payment_detail.correspondent_account = updated_payment_detail.correspondent_account
            orm_payment_detail.bik = updated_payment_detail.bik
            orm_payment_detail.bank_recipient = updated_payment_detail.bank_recipient

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'Дело обновлено. ID = {updated_payment_detail.id}')
            return PaymentDetailMapper.to_domain(orm_payment_detail)
        
        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при обновлении дела ID = {updated_payment_detail.id}: {e}')
            raise DatabaseErrorException(f'Ошибка при обновлении данных ДЕЛА: {str(e)}')
        
    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(PaymentDetailORM).where(PaymentDetailORM.id == id)
            result = await self.session.execute(stmt)
            orm_payment_detail = result.scalars().first()

            if not orm_payment_detail:
                logger.warning(f'Дело с ID {id} не найдено при удалении.')
                raise EntityNotFoundException(f'Дело с ID {id} не найдено')

            # 2. Удаление
            await self.session.delete(orm_payment_detail)
            await self.session.flush()

            logger.info(f'Дело с ID {id} успешно удалено.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении ДЕЛА: {str(e)}')