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


class ChatScenarioDBType(BaseModel):
    id: int
    chatbot_id: list[str]
    narrator_id: str
    scenario_name: str
    background: str
    created_date: Optional[datetime.datetime] = None


class ChatRoomDBType(BaseModel):
    id: int
    session_id: str
    scenario_id: int
    user_id: str
    summary: str
    created_date: Optional[datetime.datetime] = None
