import pytest
from backend.domain.entities.client import Client
from backend.core import logger
from backend.core.exceptions import (
    DatabaseErrorException,
    EntityNotFoundException,
)


class TestClientRepository:

    # ========== SAVE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_save_success(self, client_repo, sample_client):
        '''Тест успешного сохранения нового клиента'''
        save_result = await client_repo.save(sample_client)
        assert save_result is not None
        assert save_result.id is not None
        assert save_result.name == sample_client.name
        assert save_result.owner_attorney_id == sample_client.owner_attorney_id

    # ========== GET SUCCESS ==========
    @pytest.mark.asyncio
    async def test_save_and_get_success(self, client_repo, sample_client):
        '''Тест успешного сохранения и получения нового клиента'''
        save_result = await client_repo.save(sample_client)
        assert save_result is not None
        logger.debug(f'Сохранен КЛИЕНТ {save_result}')
        id = save_result.id

        client = await client_repo.get(id)
        assert client.name == sample_client.name
        assert client.owner_attorney_id == sample_client.owner_attorney_id

    # ========== SAVE DUPLICATE ==========
    @pytest.mark.asyncio
    async def test_save_duplicate(self, client_repo, sample_client):
        '''Тест попытки сохранения дубликата клиента (ожидается исключение).'''
        # 1. Сначала сохраняем исходный объект (это должно пройти успешно)
        first_save = await client_repo.save(sample_client)
        assert isinstance(first_save, Client)
        assert first_save.id is not None  # Убедимся, что ID был назначен

        # 2. Теперь пытаемся сохранить тот же объект повторно (должен вызвать исключение)
        with pytest.raises(DatabaseErrorException) as exc_info:
            await client_repo.save(sample_client)

        # 3. Проверяем сообщение исключения
        assert 'Ошибка при сохранении КЛИЕНТА' in str(exc_info.value)
        assert 'duplicate key' in str(exc_info.value).lower()  # подсказка из PostgreSQL

    # ========== UPDATE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_update_success(
        self, client_repo, sample_client, sample_update_client, persisted_attorney_id
    ):
        '''Тест успешного обновления клиента.'''
        # Вызываем метод обновления
        saved_client = await client_repo.save(sample_client)
        assert isinstance(saved_client, Client)
        assert saved_client.id is not None
        logger.debug(f'ID для сохраненного КЛИЕНТА {saved_client.id}')

        # Присваиваем ID из сохранённого объекта
        sample_update_client.id = saved_client.id
        sample_update_client.owner_attorney_id = persisted_attorney_id

        update_client = await client_repo.update(sample_update_client)

        assert update_client.name == sample_update_client.name
        assert update_client.type == sample_update_client.type
        assert update_client.email == sample_update_client.email
        assert update_client.phone == sample_update_client.phone
        assert update_client.personal_info == sample_update_client.personal_info
        assert update_client.address == sample_update_client.address
        assert update_client.messenger == sample_update_client.messenger
        assert update_client.messenger_handle == sample_update_client.messenger_handle

    # ========== FAILED UPDATE, NONEXIST CLIENT ==========
    @pytest.mark.asyncio
    async def test_update_nonexistent(self, client_repo, sample_update_client):
        '''Тест обновления несуществующего клиента (ожидается исключение).'''
        sample_update_client.id = 99999  # Несуществующий ID
        with pytest.raises(EntityNotFoundException):
            await client_repo.update(sample_update_client)

    # ========== GET ALL FOR ATTORNEY ==========
    @pytest.mark.asyncio
    async def test_get_all_for_attorney_success(
        self, client_repo, clients_list, persisted_attorney_id
    ):
        '''Тест успешного получения всех клиентов для адвоката'''
        for client in clients_list:
            await client_repo.save(client)

        get_clients = await client_repo.get_all_for_attorney(persisted_attorney_id)
        assert len(get_clients) == len(clients_list)
        for client in get_clients:
            logger.info(
                f'ID клиента = {client.id}; ID юриста = {client.owner_attorney_id}'
            )
            assert client.owner_attorney_id == persisted_attorney_id

    # ========== GET FOR CASE ==========
    @pytest.mark.asyncio
    async def test_get_for_case_success(
        self, client_repo, case_repo, sample_client, persisted_attorney_id
    ):
        '''Тест успешного получения клиента для дела'''
        from backend.domain.entities.case import Case
        from backend.domain.entities.auxiliary import CaseStatus

        # Сохраняем клиента
        saved_client = await client_repo.save(sample_client)
        assert saved_client.id is not None

        # Создаем дело с привязкой к клиенту
        test_case = Case(
            id=None,
            name='Дело о краже',
            client_id=saved_client.id,
            attorney_id=persisted_attorney_id,
            status=CaseStatus.IN_PROGRESS,
            description='Описание дела о краже',
        )
        saved_case = await case_repo.save(test_case)
        assert saved_case.id is not None

        # Получаем клиентов для дела
        clients_for_case = await client_repo.get_for_case(saved_case.id)
        assert len(clients_for_case) == 1
        assert clients_for_case[0].id == saved_client.id
        assert clients_for_case[0].name == sample_client.name

    # ========== GET BY EMAIL FOR OWNER ==========
    @pytest.mark.asyncio
    async def test_get_by_email_for_owner(
        self, client_repo, sample_client, persisted_attorney_id
    ):
        '''Тест успешного получения клиента по email для конкретного адвоката'''
        save_result = await client_repo.save(sample_client)
        assert save_result is not None
        logger.debug(f'Сохранен КЛИЕНТ {save_result}. Email - {save_result.email}')
        email = save_result.email

        client = await client_repo.get_by_email_for_owner(email, persisted_attorney_id)
        assert email == client.email
        assert client.owner_attorney_id == persisted_attorney_id

    # ========== GET BY PHONE FOR OWNER ==========
    @pytest.mark.asyncio
    async def test_get_by_phone_for_owner(
        self, client_repo, sample_client, persisted_attorney_id
    ):
        '''Тест успешного получения клиента по телефону для конкретного адвоката'''
        save_result = await client_repo.save(sample_client)
        assert save_result is not None
        logger.debug(f'Сохранен КЛИЕНТ {save_result}. Phone - {save_result.phone}')
        phone = save_result.phone

        client = await client_repo.get_by_phone_for_owner(phone, persisted_attorney_id)
        assert phone == client.phone
        assert client.owner_attorney_id == persisted_attorney_id

    # ========== GET BY PERSONAL INFO FOR OWNER ==========
    @pytest.mark.asyncio
    async def test_get_by_personal_info_for_owner(
        self, client_repo, sample_client, persisted_attorney_id
    ):
        '''Тест успешного получения клиента по персональным данным для конкретного адвоката'''
        save_result = await client_repo.save(sample_client)
        assert save_result is not None
        logger.debug(
            f'Сохранен КЛИЕНТ {save_result}. Personal info - {save_result.personal_info}'
        )
        personal_info = save_result.personal_info

        client = await client_repo.get_by_personal_info_for_owner(
            personal_info, persisted_attorney_id
        )
        assert personal_info == client.personal_info
        assert client.owner_attorney_id == persisted_attorney_id

    # ========== DELETE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_delete_success(self, client_repo, sample_client):
        '''Тест успешного удаления клиента'''
        # Вызываем метод удаления
        saved_client = await client_repo.save(sample_client)
        assert isinstance(saved_client, Client)
        assert saved_client.id is not None

        deleted_check = await client_repo.delete(saved_client.id)
        assert deleted_check is True
        check_empty = await client_repo.get(saved_client.id)
        logger.info(f'Запись удалилась, тут None == {check_empty}')
        assert check_empty is None
