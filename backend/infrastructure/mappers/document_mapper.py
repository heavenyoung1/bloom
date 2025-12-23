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
            mime_type=orm.mime_type,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_orm(domain: 'Document') -> DocumentORM:
        '''Конвертация доменной сущности документа в ORM модель.'''
        # Если id = None, SQLAlchemy создаст новый объект
        orm_doc = DocumentORM(
            file_name=domain.file_name,
            storage_path=domain.storage_path,
            file_size=domain.file_size,
            case_id=domain.case_id,
            attorney_id=domain.attorney_id,
            description=domain.description,
            mime_type=domain.mime_type,
        )
        # Устанавливаем id только если он не None
        if domain.id is not None:
            orm_doc.id = domain.id
        if domain.created_at is not None:
            orm_doc.created_at = domain.created_at
        if domain.updated_at is not None:
            orm_doc.updated_at = domain.updated_at
        return orm_doc
