import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

class ChatbotUserEnum(str, Enum):
    human = 'human'
    bot = 'bot'
    narrator = 'narrator'


class ChatMessageDBType(BaseModel):
    body: str
    user_id: str
    user_type: ChatbotUserEnum
    session_id: str
    bubble_id: str
    chatroom_id: int
    created_date: Optional[datetime.datetime]