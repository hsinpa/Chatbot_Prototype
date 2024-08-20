import asyncio
import uuid

from fastapi import APIRouter, BackgroundTasks
from langchain_core.output_parsers import StrOutputParser, PydanticToolsParser

from agent.ChatbotManager import ChatbotManager
from agent.MemoryManager import MemoryManager
from agent.memory.memory_type import ChatKnowledgeOpsType, Action, Category
from agent.tools.ultimate_json_parser import UltiToolsOutputParser
from agent.tools.weather_tool import weather_tool, WeatherToolType, WeatherOutputParser
from database.chatbot_memory_db import ChatbotMemoryDB
from database.chatbot_messages_db import ChatbotMessagesDB
from router.chatbot_route_model import ChatbotInput
from utility.simple_prompt_factory import SimplePromptFactory
from websocket.websocket_manager import get_websocket

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

memory_manager = MemoryManager()
chatbot_manager = ChatbotManager(memory_manager=memory_manager, websockets=get_websocket())


@router.post("/chat")
async def chat(c_input: ChatbotInput):
    return await chatbot_manager.achat(c_input)


@router.post("/chat_stream")
def chat_stream(c_input: ChatbotInput, background_tasks: BackgroundTasks):
    background_tasks.add_task(chatbot_manager.achat_stream, c_input)

    return {'token': c_input.token}


@router.get('/message_history/user/{user_id}/session/{session_id}')
async def get_message_history(user_id: str, session_id: str):
    message_db = ChatbotMessagesDB()
    f_messages = message_db.get_messages(user_id=user_id, session_id=session_id)

    return f_messages


@router.get('/memory/user/{user_id}/session/{session_id}')
def get_message_history(user_id: str, session_id: str):
    memory_db = ChatbotMemoryDB()

    f_messages = asyncio.run(memory_db.get_by_session_id(user_id=user_id, session_id=session_id))

    return f_messages


@router.get('/test_tool_calling')
async def test_tool_calling():
    test_factory = SimplePromptFactory(tools_calling=[weather_tool])
    test_chain = test_factory.create_chain(output_parser=WeatherOutputParser(),
                                           human_prompt_text='''What is the weather today in Taiwan, at 8pm''',
                                           )

    r = await test_chain.ainvoke({})

    return False
