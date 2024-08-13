from datetime import datetime
from enum import Enum
from typing import TypedDict, Annotated, Any

from pydantic import BaseModel, Field

from model.chatbot_model import ChatbotUserEnum


def annotate_list(x: list[Any], y: list[Any]):
    if x is None:
        x = []

    x.extend(y)
    return x


class DataChunkType(str, Enum):
    Chunk = 'chunk'
    Complete = 'complete'


class StreamingDataChunkType(BaseModel):
    session_id: str = Field(..., description='Session id, for websocket connection')
    token: str = Field(..., description='One time token to track individual request')
    data: str = Field(..., description='Actual chunk data')
    source_id: str = Field(..., description='The ID of human or bot')
    bubble_id: str = Field(..., description="ID for individual message bubble")
    index: int = Field(..., description="Order / Sequence")
    time: float = Field(..., description='UTC timestamp')
    identity: ChatbotUserEnum = Field(..., description='User Identity of this streaming message')
    type: DataChunkType


class ChatbotAgentState(TypedDict):
    final_message: Annotated[list[StreamingDataChunkType], annotate_list]
    scenario: Annotated[str, lambda x, y: y]
    query: str
    intention: str
    chatbot_id: str
    chatroom_id: int
    new_chatroom_summary: str


class General_Bullet_Point_Type(BaseModel):
    thought: str = Field(..., description='Why and what you think is important in the given context')
    points: list[str] = Field(..., description='A array of important point, highly worth mentioning')
