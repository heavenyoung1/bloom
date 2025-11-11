import pytest
from backend.domain.entities.document import Document
from backend.infrastructure.mappers import DocumentMapper
from backend.core import logger
from pathlib import Path
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


class TestDocumentMetaRepository:
    # -------- SAVE --------
    @pytest.mark.asyncio
    async def test_save_success(self, document_repo, sample_document):
        document = await document_repo.save(sample_document)
        assert isinstance(document, Document)

    # -------- SAVE DUPLICATE --------
    @pytest.mark.asyncio
    async def test_save_duplicate(self, document_repo, sample_document):
        first_save = await document_repo.save(sample_document)
        assert isinstance(first_save, Document)
        assert first_save.id is not None

        # 2. Теперь пытаемся сохранить тот же объект повторно (должен вызвать исключение)
        with pytest.raises(DatabaseErrorException) as exc_info:
            await document_repo.save(sample_document)

        # 3. Проверяем сообщение исключения
        assert 'Ошибка при сохранении МЕТАДАННЫХ ДОКУМЕНТА' in str(exc_info.value)
        assert 'duplicate key' in str(exc_info.value).lower()  # подсказка из PostgreSQL

    @pytest.mark.asyncio
    async def test_get_success(self, document_repo, sample_document):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод сохранения
        saved_document = await document_repo.save(sample_document)
        assert isinstance(saved_document, Document)
        get_document = await document_repo.get(saved_document.id)

        assert get_document.id == sample_document.id
        assert get_document.file_name == sample_document.file_name
        assert get_document.storage_path == sample_document.storage_path
        assert get_document.case_id == sample_document.case_id
        assert get_document.attorney_id == sample_document.attorney_id
        assert get_document.description == sample_document.description

    @pytest.mark.asyncio
    async def test_get_all_success(self, document_repo, documents_list, persisted_case):
        for i in documents_list:
            await document_repo.save(i)

        get_documents = await document_repo.get_all_for_case(persisted_case)
        assert len(get_documents) == len(documents_list)
        for i in get_documents:
            logger.debug(f'DOCUMENT FILE NAME  {i.file_name}')

    @pytest.mark.asyncio
    async def test_update_success(
        self, document_repo, sample_document, sample_update_document, persisted_case
    ):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        # Вызываем метод обновления
        saved_document = await document_repo.save(sample_document)
        assert isinstance(saved_document, Document)
        assert saved_document.id is not None

        # Проверяем данные до их изменения
        assert saved_document.file_name == sample_document.file_name
        assert saved_document.storage_path == sample_document.storage_path
        assert saved_document.case_id == sample_document.case_id
        assert saved_document.attorney_id == sample_document.attorney_id
        assert saved_document.description == sample_document.description

        # Присваиваем ID из сохранённого объекта в sample_update_client
        sample_update_document.id = saved_document.id
        logger.debug(f'SAMPLE DOCUMENT {sample_update_document}')

        updated_document = await document_repo.update(sample_update_document)

        # Проверяем данные после изменения
        assert updated_document.file_name == sample_update_document.file_name
        assert updated_document.storage_path == sample_update_document.storage_path
        assert updated_document.case_id == sample_update_document.case_id
        assert updated_document.attorney_id == sample_update_document.attorney_id
        assert updated_document.description == sample_update_document.description

    @pytest.mark.asyncio
    async def test_delete_success(self, document_repo, sample_document):
        '''Тест: Удаление связанного с делом документа.'''
        # Вызываем метод удаления
        saved_document = await document_repo.save(sample_document)
        assert isinstance(sample_document, Document)
        assert sample_document.id is not None

        deleted_check = await document_repo.delete(sample_document.id)
        assert deleted_check is True
        check_empty = await document_repo.get(sample_document.id)
        logger.info(f'Запись удалилась, тут None == {check_empty}')
        assert check_empty is None
