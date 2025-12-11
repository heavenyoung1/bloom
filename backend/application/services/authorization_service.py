from backend.core.logger import logger
from backend.core.exceptions import AccessDeniedException


class AuthorizationService:
    '''
    Сервис для проверки прав доступа.

    ⚠️ Все методы stateless (без state), используются как утилиты.
    Поэтому можно использовать @staticmethod.
    '''

    # ========== OWNER ACCESS ==========

    @staticmethod
    def check_owner_access(
        current_attorney_id: int,
        owner_attorney_id: int,
        resource_type: str = 'ресурс',
        resource_id: int = None,
    ) -> None:
        '''
        Проверить что текущий адвокат является владельцем ресурса.

        Используется в:
        - DeleteClientUseCase
        - UpdateClientUseCase
        - GetClientUseCase
        - DeleteCaseUseCase
        - UpdateCaseUseCase
        - GetCaseUseCase
        - И везде где нужна проверка владельца

        Args:
            current_attorney_id: ID текущего адвоката (из JWT)
            owner_attorney_id: ID владельца ресурса
            resource_type: Тип ресурса для логирования (Client, Case и т.д.)
            resource_id: ID ресурса для логирования

        Raises:
            AccessDeniedException: Если нет доступа

        Example:
            AuthorizationService.check_owner_access(
                current_attorney_id=current_id,
                owner_attorney_id=client.owner_attorney_id,
                resource_type='Client',
                resource_id=client_id
            )
        '''
        if owner_attorney_id != current_attorney_id:
            log_msg = f'Попытка доступа к {resource_type}'
            if resource_id:
                log_msg += f' ID={resource_id}'
            log_msg += f' (владелец={owner_attorney_id}, текущий={current_attorney_id})'

            logger.warning(log_msg)

            raise AccessDeniedException(
                f'У вас нет прав доступа к этому {resource_type}'
            )

    # ========== SELF ACCESS ==========

    @staticmethod
    def check_self_access(
        current_attorney_id: int,
        target_attorney_id: int,
    ) -> None:
        '''
        Проверить что адвокат может только редактировать/удалять свой профиль.

        Используется в:
        - UpdateAttorneyUseCase (обновление профиля)
        - ChangePasswordUseCase (изменение пароля)
        - DeleteAccountUseCase (удаление учетной записи)

        Args:
            current_attorney_id: ID текущего адвоката
            target_attorney_id: ID целевого адвоката

        Raises:
            AccessDeniedException: Если пытается редактировать чужой профиль

        Example:
            AuthorizationService.check_self_access(
                current_attorney_id=current_id,
                target_attorney_id=cmd.attorney_id
            )
        '''
        if current_attorney_id != target_attorney_id:
            logger.warning(
                f'Попытка редактирования чужого профиля '
                f'(текущий={current_attorney_id}, целевой={target_attorney_id})'
            )

            raise AccessDeniedException('Вы можете редактировать только свой профиль')

    # ========== SUPERUSER ACCESS ==========

    @staticmethod
    def check_superuser_access(is_superuser: bool) -> None:
        '''
        Проверить что адвокат имеет права администратора.

        Используется в:
        - Админ операции (если будут)

        Args:
            is_superuser: Флаг суперпользователя

        Raises:
            AccessDeniedException: Если не суперпользователь

        Example:
            AuthorizationService.check_superuser_access(current_attorney.is_superuser)
        '''
        if not is_superuser:
            logger.warning('Попытка доступа к функции для администраторов')

            raise AccessDeniedException('Эта операция доступна только администраторам')
