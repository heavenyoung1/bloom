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
        '''Тест успешного сохранения нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        assert save_result.id == sample_attorney.id
        assert save_result.license_id == sample_attorney.license_id

    # -------- SAVE AND GET --------
    @pytest.mark.asyncio
    async def test_save_and_get_success(self, attorney_repo, sample_attorney):
        '''Тест: сохранение + получение по ID.'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}')
        id = save_result.id

        attorney = await attorney_repo.get(id)
        assert attorney.license_id == sample_attorney.license_id

    # -------- SAVE DUPLICATE --------
    @pytest.mark.asyncio
    async def test_save_duplicate(self, attorney_repo, sample_attorney):
        '''Тест попытки сохранения дубликата адвоката (ожидается исключение).'''
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
        '''Тест успешного обновления адвоката.'''
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
        assert update_attorney.hashed_password == sample_update_attorney.hashed_password

    @pytest.mark.asyncio
    async def test_update_nonexistent(self, attorney_repo, sample_update_attorney):
        '''Тест обновления несуществующего адвоката (ожидается исключение).'''
        with pytest.raises(EntityNotFoundException):
            await attorney_repo.update(sample_update_attorney)

    # -------- GET BY EMAIL --------
    @pytest.mark.asyncio
    async def test_get_by_email(self, attorney_repo, sample_attorney):
        '''Тест получения адвоката по email (успешный случай).'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}. Email - {save_result.email}')
        email = save_result.email

        attorney = await attorney_repo.get_by_email(email)
        assert email == attorney.email

    # @pytest.mark.asyncio
    # async def test_get_by_email_not_found(self, attorney_repo):
    #     '''Тест получения адвоката по несуществующему email (ожидается исключение).'''
    #     with pytest.raises(EntityNotFoundException):
    #         await attorney_repo.get_by_email('nonexistent@example.com')

    # -------- GET BY LICENSE ID --------
    @pytest.mark.asyncio
    async def test_get_by_license_id(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}')
        license_id = save_result.license_id

        attorney = await attorney_repo.get_by_license_id(license_id)
        assert license_id == attorney.license_id

    # @pytest.mark.asyncio
    # async def test_get_by_license_id_not_found(self, attorney_repo):
    #     '''Тест получения адвоката по несуществующему license_id (ожидается исключение).'''
    #     with pytest.raises(EntityNotFoundException):
    #         await attorney_repo.get_by_license_id('nonexistent_license')

    # -------- GET BY PHONE --------
    @pytest.mark.asyncio
    async def test_get_by_phone(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}')
        phone_number = save_result.phone

        attorney = await attorney_repo.get_by_phone(phone_number)
        assert phone_number == attorney.phone

    # @pytest.mark.asyncio
    # async def test_get_by_phone_not_found(self, attorney_repo):
    #     '''Тест получения адвоката по несуществующему phone (ожидается исключение).'''
    #     with pytest.raises(EntityNotFoundException):
    #         await attorney_repo.get_by_phone('+79990000000')
