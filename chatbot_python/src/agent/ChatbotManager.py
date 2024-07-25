import uuid

from agent.agent_utility import streaming_exec
from agent.chatbot.ChatbotGraphAgent import ChatbotGraphAgent
from agent.chatbot.chatbot_type import StreamingDataChunkType, DataChunkType
from agent.memory.memory_agent import MemoryGraphAgent
from database.chatbot_messages_db import ChatbotMessagesDB
from database.chatroom_db import ChatRoomDB
from database.db_manager import PostgresDB_Chat
from model.chatbot_model import ChatbotUserEnum, ChatMessageDBInputType, ChatScenarioDBType, ChatRoomDBType
from router.chatbot_route_model import ChatbotInput, ChatbotStreamingInput
from utility.utility_method import get_langfuse_callback
from websocket.websocket_manager import WebSocketManager


class ChatbotManager:

    def __init__(self, websockets: WebSocketManager):
        self._websockets = websockets
        self.chatbot_message_db = ChatbotMessagesDB()
        self.chatroom_db = ChatRoomDB()

    def get_chat_graph(self, c_input: ChatbotInput, scenario_db_type: ChatScenarioDBType,
                       chatroom_db_type: ChatRoomDBType):
        chat_agent = ChatbotGraphAgent(name='Honey', personality='naughty', goal='teach fruit knowledge',
                                       background='Once a school teacher, now out of job',
                                       chatroom_summary=chatroom_db_type.summary,
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
        # Prepare dataset
        scenario_db_type: ChatScenarioDBType = ChatScenarioDBType(**self.chatroom_db.get_scenario_info(scenario_id=1))
        chatroom_db_type: ChatRoomDBType = self.chatroom_db.get_chatroom_id(user_id=c_input.user_id,
                                                                            scenario_id=scenario_db_type.id,
                                                                            session_id=c_input.session_id)

        chat_graph = self.get_chat_graph(c_input, scenario_db_type, chatroom_db_type)

        result = await chat_graph.ainvoke({'query': c_input.text})

        bot_message: StreamingDataChunkType = result['final_message']

        messages = self._save_message_to_db(c_input, chatroom_db_type, bot_message)
        self.chatbot_message_db.update_summary(chatroom_db_type.id, result['new_chatroom_summary'])

        memory_agent = MemoryGraphAgent(chatroom_id=chatroom_db_type.id, messages=messages)
        memory_graph = memory_agent.create_graph().with_config({'callbacks': [get_langfuse_callback()]})
        await memory_graph.ainvoke({'messages': messages})

        return result

    # * DB Operation
    def _save_message_to_db(self, c_input: ChatbotInput, chatroom_db: ChatRoomDBType,
                            bot_message: StreamingDataChunkType):
        user_bubble_id = str(uuid.uuid4())

        insert_messages_data = [
            ChatMessageDBInputType(
                chatroom_id=chatroom_db.id, body=c_input.text,
                message_type=ChatbotUserEnum.human,
                bubble_id=user_bubble_id, user_id='hsinpa@gmail.com'
            ),
            ChatMessageDBInputType(
                chatroom_id=chatroom_db.id, body=bot_message.data,
                message_type=ChatbotUserEnum.bot,
                bubble_id=bot_message.bubble_id, user_id='0d225970-8626-4f47-8044-4f1ec5961ee7'
            ),
        ]

        # insert user
        self.chatbot_message_db.insert_message(insert_messages_data)

        return insert_messages_data
