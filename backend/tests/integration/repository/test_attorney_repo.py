import pytest
from backend.core import logger
from backend.domain.entities.attorney import Attorney

from backend.core.exceptions import (
    DatabaseErrorException,
    EntityNotFoundException,
)


class TestAttorneyRepository:

    # ========== SAVE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_save_success(self, attorney_repo, sample_attorney):
        '''Тест успешного сохранения нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        assert save_result.id == sample_attorney.id
        assert save_result.license_id == sample_attorney.license_id

    # ========== GET SUCCESS ==========
    @pytest.mark.asyncio
    async def test_save_and_get_success(self, attorney_repo, sample_attorney):
        '''Тест успешного сохранения и получения нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}')
        id = save_result.id

        attorney = await attorney_repo.get(id)
        assert attorney.license_id == sample_attorney.license_id

    # ========== SAVE DUPLICATE ==========
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

    # ========== UPDATE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_update_success(
        self, attorney_repo, sample_attorney, sample_update_attorney
    ):
        '''Тест успешного обновления юриста.'''
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

    # ========== FAILED UPDATE, NONEXIST ATTORNEY ==========
    @pytest.mark.asyncio
    async def test_update_nonexistent(self, attorney_repo, sample_update_attorney):
        '''Тест обновления несуществующего юриста (ожидается исключение).'''
        with pytest.raises(EntityNotFoundException):
            await attorney_repo.update(sample_update_attorney)

    # ========== GET BY EMAIL ==========
    @pytest.mark.asyncio
    async def test_get_by_email(self, attorney_repo, sample_attorney):
        '''Тест получения юриста по email (успешный случай).'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}. Email - {save_result.email}')
        email = save_result.email

        attorney = await attorney_repo.get_by_email(email)
        assert email == attorney.email

    # ========== GET BY EMAIL UNSUCCESS ==========
    # @pytest.mark.asyncio
    # async def test_get_by_email_not_found(self, attorney_repo):
    #     '''Тест получения адвоката по несуществующему email (ожидается исключение).'''
    #     with pytest.raises(EntityNotFoundException):
    #         await attorney_repo.get_by_email('nonexistent@example.com')

    # ========== GET BY EMAIL LICENSE_ID ==========
    @pytest.mark.asyncio
    async def test_get_by_license_id(self, attorney_repo, sample_attorney):
        '''Тест успешного получения юриста по номеру удостоверения'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}')
        license_id = save_result.license_id

        attorney = await attorney_repo.get_by_license_id(license_id)
        assert license_id == attorney.license_id

    # ========== GET BY EMAIL LICENSE_ID UNSUCCESS ==========
    # @pytest.mark.asyncio
    # async def test_get_by_license_id_not_found(self, attorney_repo):
    #     '''Тест получения адвоката по несуществующему license_id (ожидается исключение).'''
    #     with pytest.raises(EntityNotFoundException):
    #         await attorney_repo.get_by_license_id('nonexistent_license')

    # ========== GET BY EMAIL PHONE ==========
    @pytest.mark.asyncio
    async def test_get_by_phone(self, attorney_repo, sample_attorney):
        '''Тест успешного получения юриста по номеру телефона'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}')
        phone_number = save_result.phone

        attorney = await attorney_repo.get_by_phone(phone_number)
        assert phone_number == attorney.phone

    # ========== GET BY EMAIL PHONE UNSUCCESS ==========
    # @pytest.mark.asyncio
    # async def test_get_by_phone_not_found(self, attorney_repo):
    #     '''Тест получения адвоката по несуществующему phone (ожидается исключение).'''
    #     with pytest.raises(EntityNotFoundException):
    #         await attorney_repo.get_by_phone('+79990000000')

    # ========== UPDATE VERIFICATION STATUS ==========
    @pytest.mark.asyncio
    async def test_change_verify(self, attorney_repo, sample_attorney):
        '''Тест успешного изменения статуса верификации False -> True'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is not None
        logger.debug(f'Сохранен ЮРИСТ {save_result}')
        id = save_result.id

        attorney = await attorney_repo.get(id)
        assert attorney.license_id == sample_attorney.license_id
        assert attorney.is_verified == False

        verified_user = await attorney_repo.change_verify(attorney.id, True)
        assert verified_user.is_verified == True
