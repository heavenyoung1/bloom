from datetime import datetime
import pytest
from backend.domain.entities.document import Document
from backend.infrastructure.models import DocumentORM
import shutil
import tempfile

@pytest.fixture()
def temp_storage_dir():
    '''
    Создает временную директорию для файлов
    '''
    temp_dir = tempfile.mkdtemp(prefix='test_documents_')
    yield temp_dir
    # Удаляем после теста
    #shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def sample_document(test_case, persisted_attorney_id, persisted_case):
    '''
    Создает доменный объект документа для тестов
    '''
    return Document(
        id=None,
        file_name='test_contract.pdf',
        case_id=test_case.id,
        storage_path=None,
        file_size=None,
        case_id=persisted_case,
        attorney_id=persisted_attorney_id,
        description='Тестовый договор',
    )

@pytest.fixture
def sample_file_content():
    '''
    Создает тестовое содержимое файла
    '''