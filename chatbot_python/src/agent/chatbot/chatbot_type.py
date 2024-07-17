from enum import Enum
from typing import TypedDict, Annotated

from pydantic import BaseModel, Field


class ChatbotAgentState(TypedDict):
    final_message: Annotated[str, lambda x, y: y]
    query: str
    intention: str


class DataChunkType(str, Enum):
    Chunk = 'chunk'
    Complete = 'complete'


class StreamingDataChunkType(BaseModel):
    session_id: str = Field(..., description='Session id, for websocket connection')
    token: str = Field(..., description='One time token to track individual request')
    data: str = Field(..., description='Actual chunk data')
    type: DataChunkType
