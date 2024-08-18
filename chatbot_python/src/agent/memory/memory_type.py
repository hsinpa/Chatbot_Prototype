from enum import Enum
from typing import TypedDict, Annotated, Optional

from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from model.chatbot_model import ChatMessageDBInputType


class Category(str, Enum):
    Knowledge = "Knowledge"
    Item = "Item"


class Action(str, Enum):
    Create = "Create"
    Update = "Update"
    Delete = "Delete"


class ChatKnowledgeType(BaseModel):
    attribute: Category = Field(...,
                                description='Category that this knowledge belongs to. Only knowledge and item exist')
    knowledge: str = Field(..., alias='body',
                           description="""Condensed bit of knowledge to be saved for future reference in the format:
[person(s) this is relevant to] [fact to store] (e.g. Husband doesn't like tuna; I am allergic to shellfish; etc)""", )
    knowledge_id: Optional[int] = Field(-1, alias='id', description="only use for update and delete operation")


class ChatKnowledgeOpsType(ChatKnowledgeType):
    action: Action = Field(...,
                           description='Whether this knowledge is adding a new record, updating a record, or deleting a record')


class ChatNewKnowledgeType(BaseModel):
    thought: str = Field(...,
                         description='Analyze the message for new information, in contrast to what user already know')
    result: bool = Field(...,
                         description='If it has any information worth recording, return TRUE. If not, return FALSE')


class ChatbotMemoryState(TypedDict):
    messages: Annotated[list[ChatMessageDBInputType], lambda x, y: y]
    new_knowledge: ChatNewKnowledgeType
    knowledge_ops: list[ChatKnowledgeOpsType]


@tool(args_schema=ChatKnowledgeOpsType, return_direct=True)
def knowledge_ops_facade_tool(attribute: Category, action: Action, knowledge: str, knowledge_id: Optional[int]) -> bool:
    """A knowledge operation tool, that can create, update, delete data in a data structure"""
    return True
