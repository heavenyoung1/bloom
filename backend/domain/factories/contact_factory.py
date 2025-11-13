from backend.domain.entities.contact import Contact


class ContactFactory:
    '''Фабрика для создания Contact'''

    @staticmethod
    def create(
        *,
        name: str,
        personal_info: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        case_id: int,
    ) -> Contact:
        '''Создать новый объект Contact'''
        return Contact(
            id=None,
            name=name,
            personal_info=personal_info,
            phone=phone,
            email=email,
            case_id=case_id,
        )
