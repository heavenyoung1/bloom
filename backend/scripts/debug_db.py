import asyncio
import asyncpg


async def main():
    conn = await asyncpg.connect(
        host='192.168.175.129',
        port=5436,
        user='postgres',
        password='1234',
        database='test_db',
    )
    row = await conn.fetchrow('SELECT 1')
    print('RESULT:', row)
    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())
