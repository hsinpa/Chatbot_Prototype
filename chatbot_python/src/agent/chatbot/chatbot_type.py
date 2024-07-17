from typing import TypedDict, Annotated


class ChatbotAgentState(TypedDict):
    final_message: Annotated[str, lambda x, y: y]
    query: str
    intention: str