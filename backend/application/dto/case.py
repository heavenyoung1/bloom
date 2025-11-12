from backend.infrastructure.models.client import Messenger

from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import Optional
from datetime import datetime