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
