import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

class ChatbotUserEnum(str, Enum):
    human = 'human'
    bot = 'bot'
    narrator = 'narrator'


class ChatMessageDBInputType(BaseModel):
    body: str
    user_id: str
    message_type: ChatbotUserEnum
    bubble_id: str
    chatroom_id: int
    created_date: Optional[datetime.datetime] = None