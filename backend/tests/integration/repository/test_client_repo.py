import pytest
from backend.domain.entities.client import Client
from backend.core import logger
from backend.core.exceptions import (
    DatabaseErrorException,
)


class TestClientRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_success(self, client_repo, sample_client):
        client = await client_repo.save(sample_client)
        assert isinstance(client, Client)
        assert client.id is not None
        logger.debug(f'ID сохраненного клиента - {client.id}')
        assert client.name == sample_client.name
        assert client.owner_attorney_id == sample_client.owner_attorney_id

    # -------- SAVE DUPLICATE --------
    @pytest.mark.asyncio
    async def test_save_duplicate(self, client_repo, sample_client):
        first_save = await client_repo.save(sample_client)
        assert isinstance(first_save, Client)
        assert first_save.id is not None

        # 2. Теперь пытаемся сохранить тот же объект повторно (должен вызвать исключение)
        with pytest.raises(DatabaseErrorException) as exc_info:
            await client_repo.save(sample_client)

        # 3. Проверяем сообщение исключения
        assert 'Ошибка при сохранении КЛИЕНТА' in str(exc_info.value)
        assert 'duplicate key' in str(exc_info.value).lower()  # подсказка из PostgreSQL

    @pytest.mark.asyncio
    async def test_get_success(self, client_repo, sample_client):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод сохранения
        saved_case = await client_repo.save(sample_client)
        assert isinstance(saved_case, Client)
        get_case = await client_repo.get(saved_case.id)

        assert get_case.id == sample_client.id
        assert get_case.name == sample_client.name
        assert get_case.owner_attorney_id == sample_client.owner_attorney_id

    @pytest.mark.asyncio
    async def test_get_all_success(
        self, client_repo, clients_list, persisted_attorney_id
    ):
        for i in clients_list:
            await client_repo.save(i)

        get_clients = await client_repo.get_all_for_attorney(persisted_attorney_id)
        assert len(get_clients) == len(clients_list)
        for client in get_clients:
            logger.info(
                f'ID клиента = {client.id}; ID юриста = {client.owner_attorney_id}'
            )
            assert client.owner_attorney_id == persisted_attorney_id

    @pytest.mark.asyncio
    async def test_update_success(
        self, client_repo, sample_client, sample_update_client, persisted_attorney_id
    ):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод обновления
        saved_case = await client_repo.save(sample_client)
        assert isinstance(saved_case, Client)
        assert saved_case.id is not None

        # Проверяем данные до их изменения
        assert saved_case.name == sample_client.name
        assert saved_case.type == sample_client.type
        assert saved_case.email == sample_client.email
        assert saved_case.phone == sample_client.phone
        assert saved_case.personal_info == sample_client.personal_info

        # Присваиваем ID из сохранённого объекта в sample_update_client
        sample_update_client.id = saved_case.id

        update_client = await client_repo.update(sample_update_client)

        # Проверяем данные после изменения
        assert update_client.name == sample_update_client.name
        assert update_client.type == sample_update_client.type
        assert update_client.email == sample_update_client.email
        assert update_client.phone == sample_update_client.phone
        assert update_client.personal_info == sample_update_client.personal_info

    @pytest.mark.asyncio
    async def test_delete_success(self, client_repo, sample_client):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод удаления
        saved_client = await client_repo.save(sample_client)
        assert isinstance(saved_client, Client)
        assert saved_client.id is not None

        deleted_check = await client_repo.delete(saved_client.id)
        assert deleted_check is True
        check_empty = await client_repo.get(saved_client.id)
        logger.info(f'Запись удалилась, тут None == {check_empty}')
        assert check_empty is None
