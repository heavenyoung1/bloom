from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.services.doc_service import DocumentService
from backend.application.interfaces.repositories.local_storage import IFileStorage
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.core.logger import logger


class DeleteDocumentUseCase:
    '''Сценарий: удаление документа.'''

    def __init__(
        self, uow_factory: UnitOfWorkFactory, file_storage: IFileStorage
    ):
        self.uow_factory = uow_factory
        self.file_storage = file_storage

    async def execute(self, document_id: int, attorney_id: int) -> bool:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Проверяем, что документ существует и принадлежит юристу
                document = await uow.doc_meta_repo.get(document_id)
                if not document:
                    raise EntityNotFoundException(
                        f'Документ с ID {document_id} не найден'
                    )

                if document.attorney_id != attorney_id:
                    raise AccessDeniedException(
                        'У вас нет доступа к этому документу'
                    )

                # 2. Создаем DocumentService для удаления файла и метаданных
                doc_service = DocumentService(
                    document_repo=uow.doc_meta_repo, file_storage=self.file_storage
                )

                # 3. Удаляем документ (файл + метаданные)
                await doc_service.delete_document(document_id)

                logger.info(f'Документ удален: ID={document_id}')
                return True

            except (EntityNotFoundException, AccessDeniedException) as e:
                logger.error(f'Ошибка при удалении документа: {e}')
                raise e

            except Exception as e:
                logger.error(f'Неизвестная ошибка при удалении документа: {e}')
                raise Exception('Ошибка при удалении документа')

