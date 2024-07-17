from fastapi import APIRouter

from agent.ChatbotManager import ChatbotManager
from router.chatbot_route_model import ChatbotInput
from websocket.websocket_manager import websocket_manager

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

chatbot_manager = ChatbotManager(websockets=websocket_manager)

@router.post("/chat")
async def chat(c_input: ChatbotInput):
    return await chatbot_manager.achat(c_input)

@router.post("/chat_stream")
async def chat_stream(c_input: ChatbotInput):
    return await chatbot_manager.achat(c_input)