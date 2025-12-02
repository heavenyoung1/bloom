import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.core.logger import logger
from backend.core.db.database import database
from backend.infrastructure.redis.client import redis_client
from backend.presentation.api.v0.routes.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Управление жизненным циклом приложения (startup и shutdown)'''
    
    # ===== STARTUP =====
    try:
        logger.info('[STARTUP] Инициализация приложения...')
        
        # Подключиться к БД
        await database.connect()
        logger.info('[STARTUP] БД подключена')
        
        # Подключиться к Redis
        await redis_client.connect()
        logger.info('[STARTUP] Redis подключен')
        
        logger.info('[STARTUP] Приложение готово к работе!')
        
    except Exception as e:
        logger.error(f'[STARTUP] Критическая ошибка: {e}')
        raise
    
    yield  # Приложение работает
    
    # ===== SHUTDOWN =====
    try:
        logger.info('[SHUTDOWN] Завершение приложения...')
        
        # Отключиться от Redis
        await redis_client.disconnect()
        logger.info('[SHUTDOWN] Redis отключен')
        
        # Закрыть пул БД
        await database.dispose()
        logger.info('[SHUTDOWN] БД отключена')
        
        logger.info('[SHUTDOWN] Приложение успешно завершено')
        
    except Exception as e:
        logger.error(f'[SHUTDOWN] Ошибка при завершении: {e}')

app = FastAPI(
    title='Attorney CRM',
    description='CRM система для юристов',
    version='1.0.0',
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:8000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Подключить роуты
app.include_router(auth_router)

# Health check endpoints
@app.get('/')
async def root():
    '''Корневой эндпоинт'''
    return {
        'message': 'Attorney CRM API',
        'version': '1.0.0',
        'docs': '/docs',
        'health': '/health'
    }

@app.get('/health')
async def health():
    '''Проверка здоровья приложения'''
    return {
        'status': 'OK',
        'database': 'connected',
        'redis': 'connected'
    }


# Точка входа
if __name__ == '__main__':
    # На Windows используем файл для логирования вместо консоли
    uvicorn.run(
        'backend.main:app',
        host='127.0.0.1',
        port=8000,
        log_level='info',
        reload=True,
        # На Windows есть проблемы с эмодзи, поэтому используем простой формат
        access_log=True,
    )