from backend.core.config import settings

print("URL (async):", settings.url())
print("URL (alembic):", settings.alembic_url())
print("host:", settings.host)
print("port:", settings.port)
print("user:", settings.user)
print("password:", settings.password)
print("db_name:", settings.db_name)

import asyncio
import asyncpg
from backend.core.config import settings

async def main():
    print("TRY CONNECT:")
    print(
        f"{settings.user=}, {settings.password=}, "
        f"{settings.host=}, {settings.port=}, {settings.db_name=}"
    )

    conn = await asyncpg.connect(
        user=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database=settings.db_name,
    )
    print("CONNECTED OK:", conn)
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
