from enum import Enum


class CaseStatus(str, Enum):
    '''Перечисление возможных статусов дела.'''

    NEW = 'Новое'  # Дело только создано, в работу ещё не принято
    IN_PROGRESS = 'В работе'  # Адвокат/юрист ведёт дело
    ON_HOLD = 'На паузе'  # Временная приостановка (ожидание клиента, документов и т.п.)
    COMPLETED = 'Завершено'  # Успешно завершено
    CLOSED = 'Закрыто'  # Закрыто без результата (например, по инициативе клиента)
    CANCELLED = 'Отменено'  # Отменено до начала работы
    ARCHIVED = 'Архивировано'  # Перемещено в архив (историческое дело)


class Messenger(str, Enum):
    TG = 'Telegram'
    WA = 'WhatsApp'
    MA = 'MAX'


class EventType(str, Enum):
    '''Типы событий'''

    meeting = 'Встреча'
    task = 'Задача'
    court_hearing = 'Судебное заседание'
    deadline = 'Дедлайн'
    important = 'Важное'
    other = 'Другое'
