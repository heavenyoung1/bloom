import pytest
from sqlmodel import select
from backend.infrastructure.models import AttorneyORM
from backend.infrastructure.mappers import AttorneyMapper
from backend.core import logger


class TestAttorneyRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_success(self, session, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is True

    # -------- SAVE AND GET --------    
    @pytest.mark.asyncio
    async def test_save_and_get_success(self, session, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is True

        orm_obj = await attorney_repo.get_by_attorney_id(sample_attorney.attorney_id)
        domain_result = AttorneyMapper.to_domain(orm_obj)
        assert domain_result.attorney_id == sample_attorney.attorney_id
        logger.info(f'ASSERTION {domain_result}')

    # -------- SAVE AND GET --------    
    @pytest.mark.asyncio
    async def test_save_duplicate(self, session, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result is True

        repeat_save_result = await attorney_repo.save(sample_attorney)
        assert repeat_save_result is False