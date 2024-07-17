from agent.chatbot.ChatbotGraphAgent import ChatbotGraphAgent
from router.chatbot_route_model import ChatbotInput
from utility.utility_method import get_langfuse_callback
from websocket.websocket_manager import WebSocketManager


class ChatbotManager:

    def __init__(self, websockets: WebSocketManager):
        self._websockets = websockets

    async def achat(self, c_input: ChatbotInput):
        chat_agent = ChatbotGraphAgent(name='Honey', personality='naughty', goal='teach fruit knowledge',
                                       background='Once a school teacher, now out of job')

        chat_graph = chat_agent.create_graph()
        chat_graph = chat_graph.with_config({'callbacks': [get_langfuse_callback()], "run_name": 'Chatbot chat chain'})

        r = await chat_graph.ainvoke({'query': c_input.text})

        return r
