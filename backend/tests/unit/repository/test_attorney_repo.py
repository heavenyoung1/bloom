import pytest
from backend.infrastructure.mappers import AttorneyMapper
from backend.core import logger


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

        attorney = await attorney_repo.get(id)
        assert attorney.attorney_id == sample_attorney.attorney_id
        #logger.debug(f'ASSERTION {attorney}')

    # -------- SAVE DUPLICATE --------
    @pytest.mark.asyncio
    async def test_save_duplicate(self, attorney_repo, sample_attorney):
        '''Тест: сохранение нового юриста'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result['success'] is True
        assert save_result['id'] is not None

        repeat_save_result = await attorney_repo.save(sample_attorney)
        assert repeat_save_result['success'] is False
        assert repeat_save_result['id'] is None

    # -------- GET BY ATTORNEY_ID --------
    @pytest.mark.asyncio
    async def test_get_by_attorney_id(self, attorney_repo, sample_attorney):
        '''Тест: получение юриста по номеру его удостоверения (attorney_id), не ID'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result['success'] is True
        attorney = await attorney_repo.get_by_attorney_id(sample_attorney.attorney_id)
        assert attorney.attorney_id == sample_attorney.attorney_id

    # -------- GET ALL ATORNEYS --------
    @pytest.mark.asyncio
    async def test_get_all_attorneys(self, attorney_repo, attorneys_list):
        '''Тест:'''
        for attorney_single in attorneys_list:
            await attorney_repo.save(AttorneyMapper.to_orm(attorney_single))

        result = await attorney_repo.get_all()
        assert len(result) == len(attorneys_list)

        # Проверка, что каждый юрист в базе имеет правильный attorney_id
        for attorney, saved_attorney in zip(result, attorneys_list):
            assert attorney.attorney_id == saved_attorney.attorney_id
            assert attorney.first_name == saved_attorney.first_name
            assert attorney.last_name == saved_attorney.last_name
            assert attorney.patronymic == saved_attorney.patronymic
            assert attorney.email == saved_attorney.email
            assert attorney.phone == saved_attorney.phone
            assert attorney.is_active == saved_attorney.is_active

    # -------- GET ALL ATORNEYS --------
    @pytest.mark.asyncio
    async def test_update_attorney(
        self, attorney_repo, sample_attorney, sample_update_attorney
    ):
        '''Тест:'''
        save_result = await attorney_repo.save(sample_attorney)
        id = save_result['id']
        assert save_result['success'] is True
        update_result = await attorney_repo.update(
            id=id, updated_attorney=sample_update_attorney
        )

        assert update_result['success'] is True
        assert update_result['attorney'].email == sample_update_attorney.email
        assert update_result['attorney'].phone == sample_update_attorney.phone
        assert (
            update_result['attorney'].password_hash
            == sample_update_attorney.password_hash
        )
        #logger.debug(f'RESULT -> {update_result['attorney']}')

    # -------- DELETE ATORNEY --------
    @pytest.mark.asyncio
    async def test_delete_attorney(self, attorney_repo, sample_attorney):
        '''Тест:'''
        save_result = await attorney_repo.save(sample_attorney)
        assert save_result['success'] is True
        id = save_result['id']
        delete_result = await attorney_repo.delete(id)
        assert delete_result is True
        get_result = await attorney_repo.get(id)
        assert get_result is None
        #logger.debug(f'RESULT -> {get_result}')
