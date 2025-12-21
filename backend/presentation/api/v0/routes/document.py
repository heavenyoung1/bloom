from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from backend.core.dependencies import (
    get_current_attorney_id,
    get_uow_factory,
    get_file_storage,
)
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.interfaces.repositories.local_storage import IFileStorage
from backend.application.usecases.document.create import CreateDocumentUseCase
from backend.application.usecases.document.get import GetDocumentByIdUseCase
from backend.application.usecases.document.get_all import GetDocumentsForCaseUseCase
from backend.application.usecases.document.delete import DeleteDocumentUseCase
from backend.application.usecases.document.download import DownloadDocumentUseCase
from backend.application.dto.document import (
    DocumentCreateRequest,
    DocumentResponse,
    DocumentListResponse,
)
from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
    AccessDeniedException,
)
from backend.core.logger import logger
from io import BytesIO

# ========== Router ==========
router = APIRouter(prefix='/api/v0', tags=['documents'])

# ========== DOCUMENT ENDPOINTS ==========


@router.post(
    '/cases/{case_id}/documents',
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Загрузка документа в дело',
    responses={
        201: {'description': 'Документ успешно загружен'},
        400: {'description': 'Ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Дело не найдено'},
    },
)
async def upload_document(
    case_id: int,
    file: UploadFile = File(..., description='Файл для загрузки'),
    description: str = Form(None, description='Описание документа'),
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
    file_storage: IFileStorage = Depends(get_file_storage),
):
    '''
    Загрузка документа в систему.

    Flow:
    1. Получение файла из запроса
    2. Валидация дела и прав доступа
    3. Сохранение файла в хранилище
    4. Извлечение метаданных (MIME тип, размер)
    5. Сохранение метаданных в БД
    6. Возврат данных документа

    Requires:
        - Authorization: Bearer <access_token>
        - multipart/form-data с полем "file"
    '''
    try:
        logger.info(
            f'Попытка загрузки документа: {file.filename} '
            f'для дела {case_id} (адвокат={current_attorney_id})'
        )

        # 1. Читаем содержимое файла
        file_content = await file.read()
        if not file_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Файл пуст',
            )

        # 2. Проверяем размер файла (например, максимум 50 МБ)
        max_file_size = 50 * 1024 * 1024  # 50 МБ
        if len(file_content) > max_file_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Размер файла превышает максимальный ({max_file_size / 1024 / 1024} МБ)',
            )

        # 3. Создаем use case и загружаем документ
        use_case = CreateDocumentUseCase(uow_factory, file_storage)
        result = await use_case.execute(
            case_id=case_id,
            attorney_id=current_attorney_id,
            file_name=file.filename,
            file_content=file_content,
            description=description or '',
        )

        logger.info(f'Документ успешно загружен: ID={result.id}, Файл={file.filename}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except EntityNotFoundException as e:
        logger.error(f'Сущность не найдена: {e}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при загрузке документа',
        )


@router.get(
    '/cases/{case_id}/documents',
    response_model=DocumentListResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение списка документов дела',
    responses={
        200: {'description': 'Список документов'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Дело не найдено'},
    },
)
async def get_case_documents(
    case_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение всех документов для дела.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(
            f'Получение документов для дела {case_id} '
            f'(адвокат={current_attorney_id})'
        )

        use_case = GetDocumentsForCaseUseCase(uow_factory)
        result = await use_case.execute(case_id, current_attorney_id)

        return result

    except EntityNotFoundException as e:
        logger.error(f'Сущность не найдена: {e}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AccessDeniedException as e:
        logger.error(f'Доступ запрещен: {e}')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении документов',
        )


@router.get(
    '/documents/{document_id}',
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение данных документа',
    responses={
        200: {'description': 'Данные документа'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Документ не найден'},
    },
)
async def get_document(
    document_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение метаданных документа по ID.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(
            f'Получение документа {document_id} (адвокат={current_attorney_id})'
        )

        use_case = GetDocumentByIdUseCase(uow_factory)
        result = await use_case.execute(document_id, current_attorney_id)

        return result

    except EntityNotFoundException as e:
        logger.error(f'Документ не найден: {e}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AccessDeniedException as e:
        logger.error(f'Доступ запрещен: {e}')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении документа',
        )


@router.get(
    '/documents/{document_id}/download',
    summary='Скачивание документа',
    responses={
        200: {'description': 'Файл документа'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Документ не найден'},
    },
)
async def download_document(
    document_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
    file_storage: IFileStorage = Depends(get_file_storage),
):
    '''
    Скачивание файла документа.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(
            f'Скачивание документа {document_id} (адвокат={current_attorney_id})'
        )

        use_case = DownloadDocumentUseCase(uow_factory, file_storage)
        file_content, file_name, mime_type = await use_case.execute(
            document_id, current_attorney_id
        )

        # Возвращаем файл как поток
        return StreamingResponse(
            BytesIO(file_content),
            media_type=mime_type,
            headers={
                'Content-Disposition': f'attachment; filename="{file_name}"',
            },
        )

    except EntityNotFoundException as e:
        logger.error(f'Документ не найден: {e}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AccessDeniedException as e:
        logger.error(f'Доступ запрещен: {e}')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при скачивании документа',
        )


@router.delete(
    '/documents/{document_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление документа',
    responses={
        204: {'description': 'Документ успешно удален'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Документ не найден'},
    },
)
async def delete_document(
    document_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
    file_storage: IFileStorage = Depends(get_file_storage),
):
    '''
    Удаление документа (файл и метаданные).

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(
            f'Удаление документа {document_id} (адвокат={current_attorney_id})'
        )

        use_case = DeleteDocumentUseCase(uow_factory, file_storage)
        await use_case.execute(document_id, current_attorney_id)

        return None

    except EntityNotFoundException as e:
        logger.error(f'Документ не найден: {e}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AccessDeniedException as e:
        logger.error(f'Доступ запрещен: {e}')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e)
        )
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при удалении документа',
        )

