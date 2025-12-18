import pytest
from backend.domain.entities.case import Case
from backend.core.logger import logger
from backend.core.exceptions import (
    DatabaseErrorException,
)


class TestCaseRepository:
    # ========== SAVE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_save_success(self, case_repo, sample_case):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод сохранения
        case = await case_repo.save(sample_case)
        assert isinstance(case, Case)

        assert case.id is not None
        assert case.client_id == sample_case.client_id
        assert case.attorney_id == sample_case.attorney_id
        assert case.description == sample_case.description

    # ========== SAVE DUPLICATE ==========
    @pytest.mark.asyncio
    async def test_save_duplicate(self, case_repo, sample_case):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # 1. Сначала сохраняем исходный объект (это должно пройти успешно)
        first_save = await case_repo.save(sample_case)
        assert isinstance(first_save, Case)
        assert first_save.id is not None  # Убедимся, что ID был назначен

        # 2. Теперь пытаемся сохранить тот же объект повторно (должен вызвать исключение)
        with pytest.raises(DatabaseErrorException) as exc_info:
            await case_repo.save(sample_case)

        # 3. Проверяем сообщение исключения
        assert 'Ошибка при сохранении ДЕЛА' in str(exc_info.value)
        assert 'duplicate key' in str(exc_info.value).lower()  # подсказка из PostgreSQL

    # ========== GET SUCCESS ==========
    @pytest.mark.asyncio
    async def test_get_success(self, case_repo, sample_case):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод сохранения
        saved_case = await case_repo.save(sample_case)
        assert isinstance(saved_case, Case)
        get_case = await case_repo.get(saved_case.id)

        assert get_case.client_id == sample_case.client_id
        assert get_case.attorney_id == sample_case.attorney_id
        assert get_case.name == sample_case.name

    # ========== GET ALL CASES SUCCESS ==========
    @pytest.mark.asyncio
    async def test_get_all_success(self, case_repo, cases_list, persisted_attorney_id):
        for i in cases_list:
            await case_repo.save(i)

        get_cases = await case_repo.get_all_for_attorney(persisted_attorney_id)
        assert len(get_cases) == len(cases_list)
        for case in get_cases:
            logger.info(f'ID юриста = {case.attorney_id}')
            assert case.attorney_id == persisted_attorney_id

    # ========== UPDATE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_update_success(self, case_repo, sample_case, sample_update_case):
        '''Тест: Обновление дела со связанными клиентом и адвокатом.'''
        # Вызываем метод обновления
        saved_case = await case_repo.save(sample_case)
        assert isinstance(saved_case, Case)
        assert saved_case.id is not None

        # Проверяем данные до их изменения
        assert saved_case.name == sample_case.name
        assert saved_case.status == sample_case.status
        assert saved_case.description == sample_case.description

        # Присваиваем ID из сохранённого объекта в sample_update_case
        sample_update_case.id = saved_case.id

        update_case = await case_repo.update(sample_update_case)

        # Проверяем данные после изменения
        assert update_case.name == sample_update_case.name
        assert update_case.status == sample_update_case.status
        assert update_case.description == sample_update_case.description

    # ========== DELETE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_delete_success(self, case_repo, sample_case):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод удаления
        saved_case = await case_repo.save(sample_case)
        assert isinstance(saved_case, Case)
        assert saved_case.id is not None

        deleted_check = await case_repo.delete(saved_case.id)
        assert deleted_check is True
        check_empty = await case_repo.get(saved_case.id)
        logger.info(f'Запись удалилась, тут None == {check_empty}')
        assert check_empty is None
