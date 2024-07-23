import uuid

from agent.agent_utility import streaming_exec
from agent.chatbot.ChatbotGraphAgent import ChatbotGraphAgent
from agent.chatbot.chatbot_type import StreamingDataChunkType, DataChunkType
from database.chatbot_messages_db import ChatbotMessagesDB
from database.db_manager import PostgresDB_Chat
from model.chatbot_model import ChatbotUserEnum, ChatMessageDBInputType
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
                                       websocket=self._websockets, chatroom_id=1
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
        user_bubble_id = str(uuid.uuid4())

        result = await chat_graph.ainvoke({'query': c_input.text})
        bot_message: StreamingDataChunkType = result['final_message']
        print(bot_message)

        # insert user
        await self.chatbot_message_db.insert_message(
            [
                ChatMessageDBInputType(
                    chatroom_id=1, body=c_input.text,
                    message_type=ChatbotUserEnum.human,
                    bubble_id=user_bubble_id, user_id='hsinpa@gmail.com'
                ),
                ChatMessageDBInputType(
                    chatroom_id=1, body=bot_message.data,
                    message_type=ChatbotUserEnum.bot,
                    bubble_id=bot_message.bubble_id, user_id='0d225970-8626-4f47-8044-4f1ec5961ee7'
                ),
            ]

        )

        return result
