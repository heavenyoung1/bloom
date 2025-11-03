import pytest
from backend.infrastructure.mappers import CaseMapper
from backend.core import logger


class TestCaseRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_success(self, case_repo, sample_case):
        '''Тест: сохранение нового дела'''
        save_result = await case_repo.save(sample_case)
        assert save_result['success'] is True
