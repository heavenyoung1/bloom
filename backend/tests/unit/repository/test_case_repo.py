import pytest
from backend.domain.entities.case import Case
from backend.infrastructure.mappers import CaseMapper
from backend.core import logger


class TestCaseRepository:
    # -------- SAVE --------
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


    # # -------- SAVE DUPLICATE --------
    # @pytest.mark.asyncio
    # async def test_save_duplicate(self, case_repo, sample_case):
    #     save_result = await case_repo.save(sample_case)
    #     assert save_result['success'] is True
    #     assert save_result['id'] is not None

    #     repeat_save_result = await case_repo.save(sample_case)
    #     assert repeat_save_result['success'] is False
    #     assert repeat_save_result['id'] is None
