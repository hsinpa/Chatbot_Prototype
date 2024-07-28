import uuid

from fastapi import APIRouter, BackgroundTasks
from langchain_core.output_parsers import StrOutputParser, PydanticToolsParser

from agent.ChatbotManager import ChatbotManager
from agent.MemoryManager import MemoryManager
from agent.tools.weather_tool import weather_tool, WeatherToolType, WeatherOutputParser
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


@router.get('/test_tool_calling')
async def test_tool_calling():
    print(weather_tool)
    test_factory = SimplePromptFactory(tools_calling=[weather_tool])
    test_chain = test_factory.create_chain(output_parser=WeatherOutputParser(),
                                           human_prompt_text='''What is the weather today in Taiwan, at 8pm''',
                                           )

    r = await test_chain.ainvoke({})

    print(r)

    return False
