import pytest
from sqlmodel import select
from backend.infrastructure.models import AttorneyORM


class TestAttorneyRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_new_attorney(self, session, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        result = await attorney_repo.save(sample_attorney)
        assert result is True

        #statement = select(AttorneyORM).where(AttorneyORM.id == sample_attorney.id)
