from typing import Annotated, TypedDict
from pydantic.v1 import BaseModel, Field

from agent.chatbot.chatbot_type import StreamingDataChunkType, annotate_list


class NarratorActionState(TypedDict):
    scenario: Annotated[str, lambda x, y: y]
    final_message: Annotated[list[StreamingDataChunkType], annotate_list]
    narrator_response: str
    validation_analysis: str
    is_valid: bool


class ActionType(BaseModel):
    thought: str = Field(..., description='Reason for your validation output')
    is_valid: bool = Field(..., description='Is the action valid')
