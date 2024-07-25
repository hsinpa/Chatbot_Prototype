from enum import Enum
from typing import TypedDict, Annotated, Optional

from pydantic import BaseModel, Field

from model.chatbot_model import ChatMessageDBInputType


class Category(str, Enum):
    Knowledge = "Knowledge"
    Item = "Item"


class Action(str, Enum):
    Create = "Create"
    Update = "Update"
    Delete = "Delete"


class ChatKnowledgeOpsType(BaseModel):
    attribute: Category = Field(..., description='Category that this knowledge belongs to. Only knowledge and item exist')
    knowledge: str = Field(...,
                           description="""Condensed bit of knowledge to be saved for future reference in the format:
[person(s) this is relevant to] [fact to store] (e.g. Husband doesn't like tuna; I am allergic to shellfish; etc)""", )
    action: Action = Field(...,
                           description='Whether this knowledge is adding a new record, updating a record, or deleting a record')
    id: Optional[str] = Field(..., description="only use for update and delete operation")


class ChatNewKnowledgeType(BaseModel):
    thought: str = Field(...,
                         description='Analyze the message for new information, in contrast to what user already know')
    result: bool = Field(...,
                         description='If it has any information worth recording, return TRUE. If not, return FALSE')


class ChatbotMemoryState(TypedDict):
    messages: Annotated[list[ChatMessageDBInputType], lambda x, y: y]
    new_knowledge: ChatNewKnowledgeType
    operation_type: ChatKnowledgeOpsType
