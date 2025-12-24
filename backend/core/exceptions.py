class BaseCustomException(Exception):
    '''Базовый класс для всех исключений в приложении.'''

    def __init__(self, message: str = 'Произошла ошибка'):
        self.message = message
        super().__init__(self.message)


class EntityAlreadyExistsError(BaseCustomException):
    '''Исключение при попытке создать сущность с уже существующим ID.'''

    pass


class AccessDeniedException(BaseCustomException):
    '''Ошибка прав доступа'''

    pass


class VerificationError(BaseCustomException):
    '''Ошибка, когда пользователь уже верифицирован.'''

    pass


class EntityNotFoundException(BaseCustomException):
    '''Ошибка, когда сущность не найдена.'''

    def __init__(self, message: str):
        '''
        Args:
            message: Полное сообщение об ошибке (например: "Контакт с ID 123 не найден")
        '''
        self.message = message
        super().__init__(self.message)

    @classmethod
    def for_entity(cls, entity_name: str, entity_id: int, context: str = '') -> 'EntityNotFoundException':
        '''
        Создает исключение для сущности с ID.
        
        Args:
            entity_name: Название сущности (например: "Юрист", "Дело", "Клиент")
            entity_id: ID сущности
            context: Опциональный контекст (например: " при удалении", " при обновлении")
        
        Example:
            raise EntityNotFoundException.for_entity("Юрист", 123)
            raise EntityNotFoundException.for_entity("Дело", 456, " при удалении")
        '''
        message = f'{entity_name} с ID {entity_id} не найден{context}.'
        return cls(message)


class DatabaseErrorException(BaseCustomException):
    '''Ошибка базы данных.'''

    def __init__(self, message: str = 'Ошибка взаимодействия с базой данных'):
        self.message = message
        super().__init__(self.message)


class ValidationException(BaseCustomException):
    '''Ошибка валидации данных.'''

    def __init__(self, message: str = 'Невалидные данные'):
        self.message = message
        super().__init__(self.message)


class FileStorageException(BaseCustomException):
    '''Ошибка сохранения файла.'''


class FileNotFound(BaseCustomException):
    pass


class FileAlreadyExists(BaseCustomException):
    pass
