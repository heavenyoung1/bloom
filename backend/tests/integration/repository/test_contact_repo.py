import pytest
from backend.domain.entities.contact import Contact
from backend.infrastructure.mappers import ContactMapper
from backend.core import logger
from backend.core.exceptions import (
    DatabaseErrorException,
    EntityNotFoundException,
    EntityAlreadyExistsError,
)

from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    DataError,
    NoResultFound,
    MultipleResultsFound,
    InvalidRequestError,
)


class TestContactRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_success(self, contact_repo, sample_contact):
        contact = await contact_repo.save(sample_contact)
        assert isinstance(contact, Contact)
        assert contact.id is not None
        assert contact.name == sample_contact.name
        assert contact.personal_info == sample_contact.personal_info
        assert contact.case_id == sample_contact.case_id
        logger.debug(f'ID сохраненного клиента - {contact.id}')

    # -------- SAVE DUPLICATE --------
    @pytest.mark.asyncio
    async def test_save_duplicate(self, contact_repo, sample_contact):
        first_save = await contact_repo.save(sample_contact)
        assert isinstance(first_save, Contact)
        assert first_save.id is not None

        # 2. Теперь пытаемся сохранить тот же объект повторно (должен вызвать исключение)
        with pytest.raises(DatabaseErrorException) as exc_info:
            await contact_repo.save(sample_contact)

        # 3. Проверяем сообщение исключения
        assert 'Ошибка при сохранении СВЯЗАННОГО КОНТАКТА' in str(exc_info.value)
        assert 'duplicate key' in str(exc_info.value).lower()  # подсказка из PostgreSQL

    @pytest.mark.asyncio
    async def test_get_success(self, contact_repo, sample_contact):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод сохранения
        saved_contact = await contact_repo.save(sample_contact)
        assert isinstance(saved_contact, Contact)
        get_contact = await contact_repo.get(saved_contact.id)

        assert get_contact.id == sample_contact.id
        assert get_contact.name == sample_contact.name
        assert get_contact.case_id == sample_contact.case_id

    @pytest.mark.asyncio
    async def test_get_all_success(self, contact_repo, contacts_list, persisted_case):
        for i in contacts_list:
            await contact_repo.save(i)

        get_contacts = await contact_repo.get_all_for_case(persisted_case)
        assert len(get_contacts) == len(contacts_list)

    @pytest.mark.asyncio
    async def test_update_success(
        self, contact_repo, sample_contact, sample_update_contact, persisted_case
    ):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод обновления
        saved_contact = await contact_repo.save(sample_contact)
        assert isinstance(saved_contact, Contact)
        assert saved_contact.id is not None

        # Проверяем данные до их изменения
        assert saved_contact.name == sample_contact.name
        assert saved_contact.personal_info == sample_contact.personal_info
        assert saved_contact.phone == sample_contact.phone
        assert saved_contact.email == sample_contact.email
        assert saved_contact.case_id == sample_contact.case_id

        # Присваиваем ID из сохранённого объекта в sample_update_client
        sample_update_contact.id = saved_contact.id
        logger.debug(f'SAMPLE CONTACT {sample_update_contact}')

        update_contact = await contact_repo.update(sample_update_contact)

        # Проверяем данные после изменения
        assert update_contact.name == sample_update_contact.name
        assert update_contact.personal_info == sample_update_contact.personal_info
        assert update_contact.phone == sample_update_contact.phone
        assert update_contact.email == sample_update_contact.email
        assert update_contact.case_id == sample_update_contact.case_id

    @pytest.mark.asyncio
    async def test_delete_success(self, contact_repo, sample_contact):
        '''Тест: Сохранение связанного с делом контакта.'''
        # Вызываем метод удаления
        saved_contact = await contact_repo.save(sample_contact)
        assert isinstance(saved_contact, Contact)
        assert saved_contact.id is not None

        deleted_check = await contact_repo.delete(saved_contact.id)
        assert deleted_check is True
        check_empty = await contact_repo.get(saved_contact.id)
        logger.info(f'Запись удалилась, тут None == {check_empty}')
        assert check_empty is None
