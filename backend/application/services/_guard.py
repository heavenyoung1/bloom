from backend.core.exceptions import AccessDeniedException
from backend.core.logger import logger

class Guard:
    @staticmethod
    def check_access(
            owner_attorney_id: int,
            current_attorney_id: int,
    ):
        if owner_attorney_id != current_attorney_id:
            logger.warning(f'ACCESS DENIED: У ВАС НЕТ ДОСТУПА К ЭТОЙ СУЩНОСТИ!')
            raise AccessDeniedException('ACCESS DENIED: У ВАС НЕТ ДОСТУПА К ЭТОЙ СУЩНОСТИ!')