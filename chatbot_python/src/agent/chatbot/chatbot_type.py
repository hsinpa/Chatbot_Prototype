from datetime import datetime
from enum import Enum
from typing import TypedDict, Annotated

from pydantic import BaseModel, Field


class DataChunkType(str, Enum):
    Chunk = 'chunk'
    Complete = 'complete'


class StreamingDataChunkType(BaseModel):
    session_id: str = Field(..., description='Session id, for websocket connection')
    token: str = Field(..., description='One time token to track individual request')
    data: str = Field(..., description='Actual chunk data')
    bubble_id: str = Field(..., description="ID for individual message bubble")
    index: int = Field(..., description="Order / Sequence")
    time: float = Field(..., description='UTC timestamp')
    type: DataChunkType


class ChatbotAgentState(TypedDict):
    final_message: Annotated[StreamingDataChunkType, lambda x, y: y]
    query: str
    intention: str
