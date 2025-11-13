from backend.domain.entities.client import Client
from backend.infrastructure.models.client import Messenger


class ClientFactory:
    '''Фабрика для создания Client'''

    @staticmethod
    def create(
        *,
        name: str,
        type: bool,
        email: str | None,
        phone: str,
        personal_info: str,
        address: str,
        messenger: Messenger,
        messenger_handle: str,
        owner_attorney_id: int,
    ) -> Client:
        '''Создать новый объект Client'''
        return Client(
            id=None,
            name=name,
            type=type,
            email=email,
            phone=phone,
            personal_info=personal_info,
            address=address,
            messenger=messenger,
            messenger_handle=messenger_handle,
            owner_attorney_id=owner_attorney_id,
        )
