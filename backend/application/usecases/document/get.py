from backend.application.dto.document import DocumentResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.core.logger import logger


class GetDocumentByIdUseCase:
    '''Сценарий: получение документа по ID.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, document_id: int, attorney_id: int) -> 'DocumentResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получаем документ из БД
                document = await uow.doc_meta_repo.get(document_id)
                if not document:
                    raise EntityNotFoundException(
                        f'Документ с ID {document_id} не найден'
                    )

                # 2. Проверяем права доступа (документ должен принадлежать юристу)
                if document.attorney_id != attorney_id:
                    raise AccessDeniedException(
                        'У вас нет доступа к этому документу'
                    )

                logger.info(f'Документ получен: ID={document_id}')

                # 3. Возвращаем Response
                return DocumentResponse.model_validate(document)

            except (EntityNotFoundException, AccessDeniedException) as e:
                logger.error(f'Ошибка при получении документа: {e}')
                raise e

            except Exception as e:
                logger.error(f'Неизвестная ошибка при получении документа: {e}')
                raise Exception('Ошибка при получении документа')

