class BaseCustomException(Exception):
    '''Базовый класс для всех исключений в приложении.'''

    def __init__(self, message: str = 'Произошла ошибка'):
        self.message = message
        super().__init__(self.message)


class EntityAlreadyExistsError(BaseCustomException):
    '''Исключение при попытке создать сущность с уже существующим ID.'''

    pass


class EntityNotFoundException(BaseCustomException):
    '''Ошибка, когда сущность не найдена.'''

    def __init__(self, entity: str):
        self.message = f'{entity} не найдено'
        super().__init__(self.message)


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
