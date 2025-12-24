from backend.application.dto.document import DocumentResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.services.doc_service import DocumentService
from backend.application.interfaces.repositories.local_storage import IFileStorage
from backend.application.policy.document_policy import DocumentValidator
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class CreateDocumentUseCase:
    '''Сценарий: юрист загружает документ в систему.'''

    def __init__(self, uow_factory: UnitOfWorkFactory, file_storage: IFileStorage):
        self.uow_factory = uow_factory
        self.file_storage = file_storage

    async def execute(
        self,
        case_id: int,
        attorney_id: int,
        file_name: str,
        file_content: bytes,
        description: str = '',
    ) -> 'DocumentResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Валидация
                validator = DocumentValidator(
                    attorney_repo=uow.attorney_repo,
                    case_repo=uow.case_repo,
                    document_repo=uow.doc_meta_repo,
                )

                # Создаем временный DTO для валидации
                from backend.application.dto.document import CreateDocumentDTO

                dto = CreateDocumentDTO(
                    file_name=file_name,
                    storage_path='',  # Будет установлен в DocumentService
                    case_id=case_id,
                    attorney_id=attorney_id,
                    description=description,
                )
                await validator.validate_on_create(dto)

                # 2. Создаем DocumentService с зависимостями
                doc_service = DocumentService(
                    document_repo=uow.doc_meta_repo, file_storage=self.file_storage
                )

                # 3. Загружаем документ (файл + метаданные)
                saved_document = await doc_service.upload_document(
                    case_id=case_id,
                    attorney_id=attorney_id,
                    file_name=file_name,
                    file_content=file_content,
                    description=description,
                )

                logger.info(
                    f'Документ создан: ID={saved_document.id}, '
                    f'Файл={file_name}, Дело={case_id}'
                )

                # 4. Возвращаем Response
                return DocumentResponse.model_validate(saved_document)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании документа: {e}')
                raise e

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании документа: {e}')
                raise Exception('Ошибка при создании документа')
