class DatabaseError(Exception):
    '''Общее исключение уровня БД.'''

class TransactionError(DatabaseError):
    '''Ошибки при управлении транзакциями.'''