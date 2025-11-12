from backend.infrastructure.repositories.interfaces.document_repo import IDocumentMetadataRepository
from backend.infrastructure.repositories.interfaces.local_storage import IFileStorage

class DocumentService:
    '''
    Сервис для работы с документами.
    Координирует: сохранение метаданных в БД + сохранение файла на диск/облако
    '''
    def __init__(self, document_repo: IDocumentMetadataRepository, file_storage: IFileStorage):
        self.document_repo = document_repo
        self.file_storage = file_storage

    async def upload(self, case_id: int, file_name: str, file_content: bytes):
        '''
        1. Сохраняет файл на диск/облако
        2. Сохраняет информацию в БД
        '''
        # 1. Сохраняем файл
        file_path = f'/opt/CASES/{case_id}/{file_name}'
        saved_path = await self.file_storage.save_file(
            file_path=file_path, 
            file_content=file_content,
            )
        
        # 2. Сохраняем информацию в БД
        document_data = {
            'file_name': file_name,
            'storage_path': saved_path,
            'file_size': len(file_path),
            'case_id': case_id,
        }