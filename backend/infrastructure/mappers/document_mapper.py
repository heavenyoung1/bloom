from backend.domain.entities.document import Document
from backend.infrastructure.models import DocumentORM


class DocumentMapper:
    @staticmethod
    def to_domain(orm: DocumentORM) -> 'Document':
        '''Конвертация ORM модели документа в доменную сущность.'''
        return Document(
            id=orm.id,
            file_name=orm.file_name,
            storage_path=orm.storage_path,
            file_size=orm.file_size,
            case_id=orm.case_id,
            attorney_id=orm.attorney_id,
            description=orm.description,
            created_at=orm.created_at,
        )

    @staticmethod
    def to_orm(domain: 'Document') -> DocumentORM:
        '''Конвертация доменной сущности документа в ORM модель.'''
        return DocumentORM(
            id=domain.id,
            file_name=domain.file_name,
            storage_path=domain.storage_path,
            file_size=domain.file_size,
            case_id=domain.case_id,
            attorney_id=domain.attorney_id,
            description=domain.description,
            created_at=domain.created_at,
        )
