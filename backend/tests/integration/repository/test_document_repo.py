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

class TestDocumentRepositorySave:
    '''Тесты для метода save()'''

    @pytest.mark.asyncio
    async def test_save_success(
        self, 
        document_repo, 
        sample_document,
        sample_file_content,
        test_session,
        temp_storage_dir
        ):
        '''Успешное сохранение документа'''
        """Проверка создания директории для дела"""
        # Act
        saved_document = await document_repo.save(
            sample_document,
            sample_file_content
        )
        
        # Assert
        case_dir = Path(temp_storage_dir) / str(sample_document.case_id)
        assert case_dir.exists()
        assert case_dir.is_dir()
    
    async def test_save_document_unique_filenames(
        self,
        document_repository,
        sample_document,
        sample_file_content,
        test_session
    ):
        """Проверка уникальности имен файлов"""
        # Act - сохраняем два документа с одинаковым именем
        doc1 = await document_repository.save(
            sample_document,
            sample_file_content
        )
        await test_session.commit()
        
        # Создаем второй документ с тем же именем файла
        sample_document.id = None  # Сбрасываем ID
        doc2 = await document_repository.save(
            sample_document,
            sample_file_content
        )
        await test_session.commit()
        
        # Assert - пути должны быть разные (благодаря timestamp)
        assert doc1.file_path != doc2.file_path
        assert Path(doc1.file_path).exists()
        assert Path(doc2.file_path).exists()
    
    async def test_save_document_rollback_on_db_error(
        self,
        document_repository,
        sample_document,
        sample_file_content,
        temp_storage_dir
    ):
        """Проверка что файл удаляется при ошибке БД"""
        # Arrange - создаем невалидный документ (несуществующий case_id)
        sample_document.case_id = 99999  # Несуществующее дело
        
        # Act & Assert
        with pytest.raises(DatabaseErrorException):
            await document_repository.save(sample_document, sample_file_content)
        
        # Проверяем что файл не остался в системе
        case_dir = Path(temp_storage_dir) / "99999"
        if case_dir.exists():
            assert len(list(case_dir.iterdir())) == 0