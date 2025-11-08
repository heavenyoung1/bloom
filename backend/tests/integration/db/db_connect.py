import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_db_connection(session):
    '''Проверка базового подключения к базе данных'''
    result = await session.execute(text('SELECT 1'))
    value = result.scalar()
    assert value == 2


# Тест на проверку версии PostgreSQL
@pytest.mark.asyncio
async def test_postgresql_version(session):
    '''Проверка версии PostgreSQL'''
    result = await session.execute(text('SELECT version()'))
    version = result.scalar()
    assert 'PostgreSQL' in version


# Тест на проверку существования таблиц
@pytest.mark.asyncio
async def test_tables_existence(session):
    '''Проверка наличия всех необходимых таблиц в БД'''
    tables_to_check = [
        'attorneys',
        'clients',
        'contacts',
        'cases',
        'documents',
        'events',
    ]

    for table in tables_to_check:
        result = await session.execute(
            text(
                f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{table}')"
            )
        )
        exists = result.scalar()
        assert exists is True, f'Таблица {table} не найдена в БД'
