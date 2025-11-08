import pytest
from backend.infrastructure.mappers import AttorneyMapper
from backend.core import logger
from backend.domain.entities.attorney import Attorney
from backend.infrastructure.models.attorney import AttorneyORM
from sqlalchemy.future import select

from backend.core.exceptions import (
    DatabaseErrorException,
    EntityNotFoundException,
    EntityAlreadyExistsError,
)

from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
)


class TestAttorneyRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_success(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        assert save_result.attorney_id == sample_attorney.attorney_id

    # -------- SAVE AND GET --------
    @pytest.mark.asyncio
    async def test_save_and_get_success(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}')
        id = save_result.id

        attorney = await attorney_repo.get(id)
        assert attorney.attorney_id == sample_attorney.attorney_id

    # -------- SAVE DUPLICATE --------
    @pytest.mark.asyncio
    async def test_save_duplicate(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        # 1. Сначала сохраняем исходный объект (это должно пройти успешно)
        first_save = await attorney_repo.save(sample_attorney)
        assert isinstance(first_save, Attorney)
        assert first_save.id is not None  # Убедимся, что ID был назначен

        # 2. Теперь пытаемся сохранить тот же объект повторно (должен вызвать исключение)
        with pytest.raises(DatabaseErrorException) as exc_info:
            await attorney_repo.save(sample_attorney)

        # 3. Проверяем сообщение исключения
        assert 'Ошибка при сохранении ЮРИСТА' in str(exc_info.value)
        assert 'duplicate key' in str(exc_info.value).lower()  # подсказка из PostgreSQL

    @pytest.mark.asyncio
    async def test_update_success(
        self, attorney_repo, sample_attorney, sample_update_attorney
    ):
        # Вызываем метод обновления
        saved_attorney = await attorney_repo.save(sample_attorney)
        assert isinstance(saved_attorney, Attorney)
        assert saved_attorney.id is not None
        # logger.debug(f'ID для сохраненного ЮРИСТА {saved_attorney.id}')

        # Присваиваем ID из сохранённого объекта
        sample_update_attorney.id = saved_attorney.id
        logger.debug(f'ID для сохраненного ЮРИСТА {saved_attorney.id}')

        update_attorney = await attorney_repo.update(sample_update_attorney)

        assert update_attorney.first_name == sample_update_attorney.first_name
        assert update_attorney.last_name == sample_update_attorney.last_name
        assert update_attorney.patronymic == sample_update_attorney.patronymic
        assert update_attorney.email == sample_update_attorney.email
        assert update_attorney.phone == sample_update_attorney.phone
        assert update_attorney.password_hash == sample_update_attorney.password_hash

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalars().first()

            if not orm_attorney:
                logger.warning(f'ЮРИСТ с ID {id} не найден при удалении.')
                raise EntityNotFoundException(
                    f'ЮРИСТ с ID {id} не найден при удалении.'
                )

            # 2. Удаление
            await self.session.delete(orm_attorney)
            await self.session.flush()

            logger.info(f'ЮРИСТ с ID {id} успешно удалено.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении ЮРИСТА: {str(e)}')
