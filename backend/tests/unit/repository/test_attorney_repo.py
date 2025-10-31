import pytest
from sqlmodel import select
from backend.infrastructure.models import AttorneyORM
from backend.infrastructure.mappers import AttorneyMapper
from backend.core import logger
from backend.core.exceptions import DatabaseErrorException


class TestAttorneyRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_success(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result['success'] is True

    # -------- SAVE AND GET --------
    @pytest.mark.asyncio
    async def test_save_and_get_success(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result['success'] is True
        id = save_result['id']

        orm_obj = await attorney_repo.get(id)
        domain_result = AttorneyMapper.to_domain(orm_obj)
        assert domain_result.attorney_id == sample_attorney.attorney_id
        logger.info(f'ASSERTION {domain_result}')

    # -------- SAVE DUPLICATE --------
    @pytest.mark.asyncio
    async def test_save_duplicate(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result['success'] is True
        assert save_result['id'] is not None

        repeat_save_result = await attorney_repo.save(sample_attorney)
        print(f'REPEAT {repeat_save_result}')
        assert repeat_save_result['success'] is False
        assert repeat_save_result['id'] is None
