# Реализация системы хранения документов

## Обзор

Система работы с документами реализована с использованием следующих компонентов:

1. **Хранение метаданных** - в PostgreSQL (таблица `documents`)
2. **Хранение файлов** - локальная файловая система или облачное хранилище (AWS S3)
3. **Извлечение метаданных** - автоматическое определение MIME типа и размера файла

## Архитектура

### Компоненты системы

#### 1. Domain Layer (Доменный слой)
- `backend/domain/entities/document.py` - доменная сущность Document
- Метод `Document.create()` для создания новых документов

#### 2. Infrastructure Layer (Слой инфраструктуры)

**Модели данных:**
- `backend/infrastructure/models/document.py` - ORM модель DocumentORM
- Поля: id, file_name, storage_path, file_size, mime_type, case_id, attorney_id, description

**Репозитории:**
- `backend/infrastructure/repositories/document_repo.py` - DocumentMetadataRepository
- `backend/infrastructure/repositories/local_storage.py` - LocalFileStorage (реализация IFileStorage)

**Мапперы:**
- `backend/infrastructure/mappers/document_mapper.py` - преобразование между доменом и ORM

**Утилиты:**
- `backend/infrastructure/tools/file_metadata.py` - извлечение метаданных файлов

#### 3. Application Layer (Слой приложения)

**DTO:**
- `backend/application/dto/document.py` - DocumentCreateRequest, DocumentResponse, DocumentListResponse

**Commands:**
- `backend/application/commands/document.py` - CreateDocumentCommand, DeleteDocumentCommand

**Use Cases:**
- `backend/application/usecases/document/create.py` - CreateDocumentUseCase
- `backend/application/usecases/document/get.py` - GetDocumentByIdUseCase
- `backend/application/usecases/document/get_all.py` - GetDocumentsForCaseUseCase
- `backend/application/usecases/document/delete.py` - DeleteDocumentUseCase
- `backend/application/usecases/document/download.py` - DownloadDocumentUseCase

**Services:**
- `backend/application/services/doc_service.py` - DocumentService (координация работы с файлами и метаданными)

**Policy:**
- `backend/application/policy/document_policy.py` - DocumentValidator

#### 4. Presentation Layer (Слой представления)
- `backend/presentation/api/v0/routes/document.py` - API endpoints для работы с документами

## Процесс загрузки документа

1. **Клиент отправляет POST запрос** на `/api/v0/cases/{case_id}/documents` с файлом
2. **API endpoint** получает файл через `UploadFile`
3. **CreateDocumentUseCase**:
   - Валидирует данные (существование дела, права доступа)
   - Создает `DocumentService`
4. **DocumentService.upload_document()**:
   - Извлекает метаданные (MIME тип, размер) через `FileMetadataExtractor`
   - Генерирует уникальное имя файла (UUID + расширение)
   - Сохраняет файл в хранилище через `IFileStorage.save_file()`
   - Создает доменную сущность `Document`
   - Сохраняет метаданные в БД через `DocumentMetadataRepository`
5. **Возвращает DocumentResponse** с данными загруженного документа

## Извлечение метаданных

Метаданные извлекаются автоматически при загрузке:

- **MIME тип**: определяется по содержимому файла (если доступна библиотека `python-magic`) или по расширению
- **Размер файла**: вычисляется из длины содержимого в байтах

### Использование библиотеки python-magic

Для более точного определения MIME типа можно установить:
```bash
# Ubuntu/Debian
sudo apt-get install libmagic1

# macOS
brew install libmagic

# Python пакет (опционально, если нужна более точная работа)
pip install python-magic-bin  # Windows
pip install python-magic      # Linux/macOS
```

Если библиотека не установлена, система использует стандартную библиотеку `mimetypes` для определения по расширению.

## Хранение файлов

### Локальное хранилище (текущая реализация)

**LocalFileStorage** сохраняет файлы в файловой системе:

- Базовый путь: `/opt/CRM/storage/` (настраивается через `FILE_STORAGE_BASE_PATH` в settings)
- Структура: `cases/{case_id}/{uuid}.{extension}`
- Преимущества:
  - Простота реализации
  - Нет зависимости от внешних сервисов
  - Быстрый доступ
- Недостатки:
  - Нужно управлять бэкапами
  - Ограничен масштабированием одного сервера

### Облачное хранилище (AWS S3)

Для использования AWS S3:

1. Создать реализацию `S3FileStorage`, наследующую `IFileStorage`
2. Установить `boto3`: `pip install boto3`
3. Настроить credentials AWS в `.env`:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_REGION=us-east-1
   AWS_S3_BUCKET_NAME=your-bucket-name
   ```
4. Изменить `get_file_storage()` в `backend/core/dependencies.py` для использования S3

**Преимущества S3:**
- Масштабируемость
- Надежность и репликация
- Интеграция с CDN
- Версионирование файлов
- Lifecycle policies

## API Endpoints

### 1. Загрузка документа
```
POST /api/v0/cases/{case_id}/documents
Content-Type: multipart/form-data

Body:
- file: файл (обязательно)
- description: описание (опционально)

Response: DocumentResponse (201)
```

### 2. Получение списка документов дела
```
GET /api/v0/cases/{case_id}/documents

Response: DocumentListResponse (200)
```

### 3. Получение документа по ID
```
GET /api/v0/documents/{document_id}

Response: DocumentResponse (200)
```

### 4. Скачивание документа
```
GET /api/v0/documents/{document_id}/download

Response: файл (200)
Headers:
- Content-Type: mime_type
- Content-Disposition: attachment; filename="..."
```

### 5. Удаление документа
```
DELETE /api/v0/documents/{document_id}

Response: 204 No Content
```

## Безопасность

1. **Авторизация**: все endpoints требуют JWT токен
2. **Проверка прав доступа**: юрист может работать только со своими документами
3. **Валидация размера файла**: максимум 50 МБ (настраивается в endpoint)
4. **Уникальные имена файлов**: используются UUID для предотвращения коллизий
5. **Проверка существования связанных сущностей**: дело должно существовать

## Миграция базы данных

Необходимо добавить поле `mime_type` в таблицу `documents`:

```python
# alembic/versions/add_mime_type_to_documents.py
def upgrade():
    op.add_column('documents', 
        sa.Column('mime_type', sa.String(100), nullable=True))
    
def downgrade():
    op.drop_column('documents', 'mime_type')
```

Запуск миграции:
```bash
alembic revision --autogenerate -m "add_mime_type_to_documents"
alembic upgrade head
```

## Настройки

В `backend/core/settings.py`:

```python
FILE_STORAGE_BASE_PATH: str = '/opt/CRM/storage/'  # Базовый путь для локального хранилища
FILE_STORAGE_TYPE: str = 'local'  # 'local' или 's3'
```

## Рекомендации по размещению

### Для разработки
- Используйте локальное хранилище на диске разработчика

### Для продакшена

**Вариант 1: Локальный сервер Linux**
- Установите приложение на сервер с достаточным дисковым пространством
- Настройте регулярные бэкапы файлов
- Используйте RAID для отказоустойчивости
- Рекомендуется для небольших/средних проектов

**Вариант 2: AWS S3 (рекомендуется для масштабирования)**
- Высокая надежность и доступность
- Автоматическое резервное копирование
- Возможность интеграции с CloudFront (CDN)
- Подходит для больших проектов

**Вариант 3: Другие облачные хранилища**
- Google Cloud Storage
- Azure Blob Storage
- MinIO (S3-совместимое хранилище для self-hosted)

## Дальнейшие улучшения

1. **Версионирование документов** - сохранение истории изменений
2. **Предпросмотр документов** - генерация thumbnail для изображений
3. **Полнотекстовый поиск** - индексация содержимого PDF/DOCX
4. **Шифрование файлов** - для чувствительных документов
5. **Сжатие файлов** - автоматическое сжатие больших файлов
6. **Вирусное сканирование** - проверка загружаемых файлов
7. **Водяные знаки** - автоматическое добавление для документов

