from backend.application.dto.document import DocumentListResponse, DocumentResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.core.logger import logger


class GetDocumentsForCaseUseCase:
    '''Сценарий: получение всех документов для дела.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self, case_id: int, attorney_id: int
    ) -> 'DocumentListResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Проверяем, что дело существует и принадлежит юристу
                case = await uow.case_repo.get(case_id)
                if not case:
                    raise EntityNotFoundException(f'Дело с ID {case_id} не найдено')

                if case.attorney_id != attorney_id:
                    raise AccessDeniedException(
                        'У вас нет доступа к этому делу'
                    )

                # 2. Получаем все документы для дела
                documents = await uow.doc_meta_repo.get_all_for_case(case_id)

                logger.info(
                    f'Получены документы для дела {case_id}: '
                    f'найдено {len(documents)} документов'
                )

                # 3. Преобразуем в Response
                document_responses = [
                    DocumentResponse.model_validate(doc) for doc in documents
                ]

                return DocumentListResponse(
                    documents=document_responses, total=len(document_responses)
                )

            except (EntityNotFoundException, AccessDeniedException) as e:
                logger.error(f'Ошибка при получении документов: {e}')
                raise e

            except Exception as e:
                logger.error(f'Неизвестная ошибка при получении документов: {e}')
                raise Exception('Ошибка при получении документов')

