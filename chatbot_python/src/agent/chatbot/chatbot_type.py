from typing import TypedDict, Annotated


class ChatbotAgentState(TypedDict):
    messages: Annotated[list[str], lambda x, y: y]
    query: str
    intention: str