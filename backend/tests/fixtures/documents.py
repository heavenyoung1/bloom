from datetime import datetime
import pytest
from backend.domain.entities.document import Document
from backend.infrastructure.models import DocumentORM
import shutil
import tempfile


@pytest.fixture
def sample_document(persisted_attorney_id, persisted_case):
    '''
    Создает доменный объект документа для тестов
    '''
    return Document(
        id=None,
        file_name='test_contract.pdf',
        storage_path='/opt/documents/',
        file_size=None,
        case_id=persisted_case,
        attorney_id=persisted_attorney_id,
        description='Тестовый договор',
    )