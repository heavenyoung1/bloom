from backend.domain.entities.document import Document


class DocumentFactory:
    '''Фабрика для создания Document'''

    @staticmethod
    def create(
        *,
        file_name: str,
        storage_path: str,
        file_size: str | None = None,
        description: str | None = None,
        case_id: int | None = None,
        attorney_id: int | None = None,
    ) -> Document:
        '''Создать новый объект Document'''
        return Document(
            id=None,
            file_name=file_name,
            storage_path=storage_path,
            file_size=file_size,
            description=description,
            case_id=case_id,
            attorney_id=attorney_id,
        )
