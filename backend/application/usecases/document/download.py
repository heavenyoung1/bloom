from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.services.doc_service import DocumentService
from backend.application.interfaces.repositories.local_storage import IFileStorage
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.core.logger import logger


class DownloadDocumentUseCase:
    '''Сценарий: скачивание документа.'''

    def __init__(
        self, uow_factory: UnitOfWorkFactory, file_storage: IFileStorage
    ):
        self.uow_factory = uow_factory
        self.file_storage = file_storage

    async def execute(
        self, document_id: int, attorney_id: int
    ) -> tuple[bytes, str, str]:
        '''
        Возвращает содержимое файла, имя файла и MIME тип.

        Returns:
            Кортеж (file_content, file_name, mime_type)
        '''
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

                # 2. Создаем DocumentService для получения файла
                doc_service = DocumentService(
                    document_repo=uow.doc_meta_repo, file_storage=self.file_storage
                )

                # 3. Получаем файл
                file_content, file_name, mime_type = (
                    await doc_service.get_document_file(document_id)
                )

                logger.info(f'Документ скачан: ID={document_id}, Файл={file_name}')
                return file_content, file_name, mime_type

            except (EntityNotFoundException, AccessDeniedException) as e:
                logger.error(f'Ошибка при скачивании документа: {e}')
                raise e

            except Exception as e:
                logger.error(f'Неизвестная ошибка при скачивании документа: {e}')
                raise Exception('Ошибка при скачивании документа')

