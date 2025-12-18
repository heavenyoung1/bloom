from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
)

from backend.application.commands.event import (
    CreateEventCommand,
    UpdateEventCommand,
    DeleteEventCommand,
    GetEventQuery,
    GetEventsForAttorneyQuery,
    GetEventsForCaseQuery,
)
from backend.application.usecases.event.create import CreateEventUseCase
from backend.application.usecases.event.update import UpdateEventUseCase
from backend.application.usecases.event.delete import DeleteEventUseCase
from backend.application.usecases.event.get import (
    GetEventUseCase,
    GetEventByAttorneyUseCase,
    GetEventByCaseUseCase,
)
from backend.application.dto.event import (
    EventCreateRequest,
    EventUpdateRequest,
    EventResponse,
    EventResponseList,
)
from backend.domain.entities.auxiliary import EventType
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger

# ========== Router ==========
router = APIRouter(prefix='/api/v0', tags=['events'])


# ====== CREATE ======
@router.post(
    '/',
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового события',
)
async def create_response(
    request: EventCreateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        logger.info(f'Создание события: {request.name} (юрист={current_attorney_id})')
        cmd = CreateEventCommand(
            name=request.name,
            description=request.description,
            case_id=request.case_id,
            attorney_id=current_attorney_id,
            event_type=request.event_type,
            event_date=request.event_date,
        )
        use_case = CreateEventUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Событие успешно создано: {request.name}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Сущность не найдена: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при создании события',
        )


# ====== READ ======
router.get(
    '/events/{event_id}',
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение данных события',
    responses={
        200: {'description': 'Данные события'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Событие не найдено'},
    },
)


async def get_event(
    event_id: int,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение данных события по ID.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Получение события: ID={event_id}')

        cmd = GetEventQuery(event_id=event_id)
        use_case = GetEventUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result

    except EntityNotFoundException as e:
        logger.error(f'Событие не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении события: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении события',
        )


# ====== READ BY ATTORNEY ======
@router.get(
    '/attorney/{attorney_id}',
    response_model=List[EventResponse],
    status_code=status.HTTP_200_OK,
    summary='Получение данных события по ID юриста',
    responses={
        200: {'description': 'Данные события'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Событие не найдено'},
    },
)
async def get_events_by_attorney(
    attorney_id: int,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        cmd = GetEventsForAttorneyQuery(attorney_id=attorney_id)

        use_case = GetEventByAttorneyUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result if result else []

    except EntityNotFoundException as e:
        logger.error(f'Событие не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении события: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении события',
        )


# ====== READ BY CASE ======
@router.get(
    '/cases/{case_id}',
    response_model=List[EventResponse],
    status_code=status.HTTP_200_OK,
    summary='Получение данных события по делу',
    responses={
        200: {'description': 'Данные события'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Событие не найдено'},
    },
)
async def get_events_by_case(
    case_id: int,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
) -> List['EventResponse']:
    try:
        cmd = GetEventsForCaseQuery(case_id=case_id)

        use_case = GetEventByCaseUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result if result else []

    except EntityNotFoundException as e:
        logger.error(f'Событие не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении события: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении события',
        )


# ====== UPDATE ======
@router.put(
    '/{event_id}',
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление данных события',
    responses={
        200: {'description': 'Событие успешно обновлено'},
        400: {'description': 'Ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Событие не найдено'},
    },
)
async def update_event(
    event_id: int,
    request: EventUpdateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Обновление данных события.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        cmd = UpdateEventCommand(
            event_id=event_id,
            name=request.name,
            description=request.description,
            event_type=request.event_type,
            event_date=request.event_date,
        )
        use_case = UpdateEventUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result

    except EntityNotFoundException as e:
        logger.error(f'Событие не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при обновлении события: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при обновлении события',
        )


# ====== DELETE ======
@router.delete(
    '/{event_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление события',
    responses={
        204: {'description': 'Событие успешно удалено'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Событие не найдено'},
    },
)
async def delete_eveny(
    event_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Удаление события.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Удаление события ID = {event_id}')

        cmd = DeleteEventCommand(event_id)
        use_case = DeleteEventUseCase(uow_factory)

        await use_case.execute(cmd)

        logger.info(f'Товар успешно удален ID = {event_id}')

    except EntityNotFoundException as e:
        logger.error(f'Событие не найдено: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при удалении события: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при удалении события',
        )
