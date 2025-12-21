# Настройка для Windows

## Можно работать прямо на Windows!

Ваше приложение **уже готово работать на Windows**. Код использует `pathlib.Path`, который автоматически работает с обеими системами.

## Быстрый старт

### 1. Настройка пути для хранения файлов

Добавьте в ваш `.env` файл (в корне проекта):

```env
# Путь для хранения файлов (можно использовать относительный или абсолютный)

# Вариант 1: Относительный путь (рекомендуется)
# Файлы будут сохраняться в папку storage/ в корне проекта
FILE_STORAGE_BASE_PATH=storage/

# Вариант 2: Абсолютный путь Windows
# FILE_STORAGE_BASE_PATH=C:\Projects\bloom\storage

# Вариант 3: Для Linux (когда будете деплоить)
# FILE_STORAGE_BASE_PATH=/opt/CRM/storage/
```

**Рекомендую использовать относительный путь `storage/`** - это будет работать и на Windows, и на Linux.

### 2. Запуск сервера

```bash
# Активируйте виртуальное окружение (если используете)
# python -m venv venv
# venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux

# Запустите сервер
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Загрузка документа через FastAPI

#### Через Swagger UI (рекомендуется для тестирования):
1. Откройте `http://localhost:8000/docs`
2. Найдите endpoint `POST /api/v0/cases/{case_id}/documents`
3. Нажмите "Try it out"
4. Заполните:
   - `case_id` - ID дела
   - `file` - выберите файл для загрузки
   - `description` (опционально) - описание документа
5. Нажмите "Execute"

#### Через curl:
```bash
curl -X POST "http://localhost:8000/api/v0/cases/1/documents" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@C:\path\to\your\document.pdf" \
  -F "description=Мой документ"
```

#### Через Python (requests):
```python
import requests

url = "http://localhost:8000/api/v0/cases/1/documents"
headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}

with open("document.pdf", "rb") as f:
    files = {"file": f}
    data = {"description": "Мой документ"}
    response = requests.post(url, headers=headers, files=files, data=data)

print(response.json())
```

#### Через JavaScript/Fetch:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('description', 'Мой документ');

fetch('http://localhost:8000/api/v0/cases/1/documents', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Где сохраняются файлы на Windows?

Если вы используете `FILE_STORAGE_BASE_PATH=storage/`, файлы будут сохраняться в:
```
C:\Users\edino\OneDrive\Documents\projects\bloom\storage\cases\{case_id}\{uuid}.{extension}
```

Например:
```
C:\Users\edino\OneDrive\Documents\projects\bloom\storage\cases\1\a1b2c3d4-e5f6-7890-abcd-ef1234567890.pdf
```

## Миграция для mime_type

Перед использованием нужно добавить поле `mime_type` в базу данных:

```bash
# Создать миграцию
alembic revision --autogenerate -m "add_mime_type_to_documents"

# Применить миграцию
alembic upgrade head
```

Или создайте миграцию вручную:

```python
# alembic/versions/xxxxx_add_mime_type_to_documents.py
def upgrade():
    op.add_column('documents', 
        sa.Column('mime_type', sa.String(100), nullable=True))

def downgrade():
    op.drop_column('documents', 'mime_type')
```

## Важно для продакшена на Linux

Когда будете деплоить на Linux:
1. Просто измените `FILE_STORAGE_BASE_PATH` в `.env` на `/opt/CRM/storage/`
2. Убедитесь, что у процесса есть права на запись в эту директорию:
   ```bash
   sudo mkdir -p /opt/CRM/storage
   sudo chown -R your_user:your_user /opt/CRM/storage
   ```
3. Всё остальное работает точно так же!

## Проверка работы

1. Загрузите документ через API
2. Проверьте, что файл появился в папке `storage/cases/{case_id}/`
3. Проверьте, что метаданные сохранились в БД:
   ```sql
   SELECT id, file_name, storage_path, mime_type, file_size FROM documents;
   ```

## Все готово!

Теперь вы можете:
- ✅ Загружать документы на Windows
- ✅ Скачивать документы
- ✅ Просматривать список документов дела
- ✅ Удалять документы

Без необходимости запускать на Linux!

