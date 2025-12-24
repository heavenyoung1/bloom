from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.core.logger import logger
from backend.domain.entities.payment_detail import PaymentDetail
from backend.application.interfaces.repositories.payment_detail_repo import (
    IPaymentDetailRepository,
)
from backend.infrastructure.mappers.payment_detail_mapper import PaymentDetailMapper
from backend.infrastructure.models.payment_detail import PaymentDetailORM


class PaymentDetailRepository(IPaymentDetailRepository):

    def __init__(self, session: AsyncSession):
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

            logger.info(
                f'Платежная информация успешно сохранена. ID - {payment_detail.id}'
            )
            return payment_detail

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении платежной информации: {str(e)}')
            raise DatabaseErrorException(
                f'Ошибка при сохранении платежной информации: {str(e)}'
            )

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении платежной информации: {str(e)}')
            raise DatabaseErrorException(
                f'Ошибка при сохранении платежной информации: {str(e)}'
            )

    async def get(self, id: int) -> 'PaymentDetail':
        try:
            # 1. Получение записи из базы данных
            stmt = select(PaymentDetailORM).where(PaymentDetailORM.id == id)
            result = await self.session.execute(stmt)
            orm_payment_detail = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_payment_detail:
                return None

            # 3. Преобразование ORM объекта в доменную сущность
            payment_detail = PaymentDetailMapper.to_domain(orm_payment_detail)

            logger.info(f'Платежная информация получена. ID - {payment_detail.id}')
            return payment_detail

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении платежной информации ID = {id}: {e}')
            raise DatabaseErrorException(
                f'Ошибка при получении платежной информации: {str(e)}'
            )

    async def get_for_attorney(self, attorney_id: int) -> 'PaymentDetail':
        try:
            # 1. Получение записи из базы данных по attorney_id
            stmt = select(PaymentDetailORM).where(
                PaymentDetailORM.attorney_id == attorney_id
            )
            result = await self.session.execute(stmt)
            orm_payment_detail = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_payment_detail:
                return None

            # 3. Преобразование ORM объекта в доменную сущность
            payment_detail = PaymentDetailMapper.to_domain(orm_payment_detail)

            logger.info(
                f'Платежная информация получена для юриста. ID - {payment_detail.id}, Attorney ID - {attorney_id}'
            )
            return payment_detail

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении платежной информации для юриста ID = {attorney_id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка при получении платежной информации: {str(e)}'
            )

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
                logger.error(
                    f'Платежная информация с ID {updated_payment_detail.id} не найдена.'
                )
                raise EntityNotFoundException(
                    f'Платежная информация с ID {updated_payment_detail.id} не найдена'
                )

            # 3. Обновление полей ORM-объекта из доменной сущности
            PaymentDetailMapper.update_orm(orm_payment_detail, updated_payment_detail)

            # 4. Сохранение в БД
            await self.session.flush()

            # 5. Возврат доменного объекта
            logger.info(
                f'Платежная информация обновлена. ID = {updated_payment_detail.id}'
            )
            return PaymentDetailMapper.to_domain(orm_payment_detail)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при обновлении платежной информации ID = {updated_payment_detail.id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка при обновлении платежной информации: {str(e)}'
            )

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(PaymentDetailORM).where(PaymentDetailORM.id == id)
            result = await self.session.execute(stmt)
            orm_payment_detail = result.scalars().first()

            if not orm_payment_detail:
                logger.warning(
                    f'Платежная информация с ID {id} не найдена при удалении.'
                )
                raise EntityNotFoundException(
                    f'Платежная информация с ID {id} не найдена'
                )

            # 2. Удаление
            self.session.delete(orm_payment_detail)
            await self.session.flush()

            logger.info(f'Платежная информация с ID {id} успешно удалена.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(
                f'Ошибка при удалении платежной информации: {str(e)}'
            )
