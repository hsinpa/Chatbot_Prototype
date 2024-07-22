from agent.agent_utility import streaming_exec
from agent.chatbot.ChatbotGraphAgent import ChatbotGraphAgent
from agent.chatbot.chatbot_type import StreamingDataChunkType, DataChunkType
from database.chatbot_messages_db import ChatbotMessagesDB
from database.db_manager import PostgresDB_Chat
from router.chatbot_route_model import ChatbotInput, ChatbotStreamingInput
from utility.utility_method import get_langfuse_callback
from websocket.websocket_manager import WebSocketManager


class ChatbotManager:

    def __init__(self, websockets: WebSocketManager):
        self._websockets = websockets
        self.chatbot_message_db = ChatbotMessagesDB()


    def get_chat_graph(self, c_input: ChatbotInput):
        chat_agent = ChatbotGraphAgent(name='Honey', personality='naughty', goal='teach fruit knowledge',
                                       background='Once a school teacher, now out of job',
                                       streaming_input=ChatbotStreamingInput(session_id=c_input.session_id,
                                                                             token=c_input.token),
                                       websocket=self._websockets
                                       )

        chat_graph = chat_agent.create_graph()
        chat_graph = chat_graph.with_config({'callbacks': [get_langfuse_callback()], "run_name": 'Chatbot chat chain'})

        return chat_graph

    async def achat(self, c_input: ChatbotInput):
        chat_graph = self.get_chat_graph(c_input)
        r = await chat_graph.ainvoke({'query': c_input.text})

        return r

    async def achat_stream(self, c_input: ChatbotInput):
        chat_graph = self.get_chat_graph(c_input)
        result = await chat_graph.ainvoke({'query': c_input.text})

        print(result)
        await self.chatbot_message_db.insert_message(chatroom_id=1, )

        return result
