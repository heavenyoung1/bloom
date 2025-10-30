import pytest


class TestAttorneyRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_new_attorney(self, session, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        result = await attorney_repo.save(sample_attorney)
        await session.commit()

        assert result is True
