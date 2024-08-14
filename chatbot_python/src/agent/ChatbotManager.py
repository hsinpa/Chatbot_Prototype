import uuid

from agent.MemoryManager import MemoryManager
from agent.agent_utility import streaming_exec
from agent.chatbot.ChatbotGraphAgent import ChatbotGraphAgent
from agent.chatbot.NarratorActionAgent import NarratorActionAgent
from agent.chatbot.chatbot_type import StreamingDataChunkType, DataChunkType
from agent.memory.memory_agent import MemoryGraphAgent
from database.chatbot_messages_db import ChatbotMessagesDB
from database.chatbot_npc_db import ChatbotNpcDB
from database.chatroom_db import ChatRoomDB
from database.db_manager import PostgresDB_Chat
from model.chatbot_model import ChatbotUserEnum, ChatMessageDBInputType, ChatScenarioDBType, ChatRoomDBType, \
    ChatbotNPCDBType
from router.chatbot_route_model import ChatbotInput, ChatbotStreamingInput
from utility.utility_method import get_langfuse_callback
from websocket.websocket_manager import WebSocketManager


class ChatbotManager:

    def __init__(self, memory_manager: MemoryManager, websockets: WebSocketManager):
        self._memory = memory_manager
        self._websockets = websockets
        self.chatbot_message_db = ChatbotMessagesDB()
        self.chatroom_db = ChatRoomDB()
        self.npc_db = ChatbotNpcDB()

    def get_chat_graph(self, c_input: ChatbotInput,
                       scenario_db_type: ChatScenarioDBType,
                       bots: list[ChatbotNPCDBType], chatroom_db_type: ChatRoomDBType):
        narrator_bot = next((b for b in bots if b.type == ChatbotUserEnum.narrator.value), None)
        chat_bot = next((b for b in bots if b.type == ChatbotUserEnum.bot.value), None)

        streaming_input = ChatbotStreamingInput(session_id=c_input.session_id,
                                                token=c_input.token,
                                                websocket_id=c_input.websocket_id)

        narrator_agent = NarratorActionAgent(narrator_bot,
                                             user_action=c_input.text,
                                             scenario=scenario_db_type.background,
                                             streaming_input=streaming_input,
                                             websocket=self._websockets)

        chat_agent = ChatbotGraphAgent(chatbot=chat_bot, narrator_agent=narrator_agent,
                                       chatroom_summary=chatroom_db_type.summary,
                                       streaming_input=streaming_input,
                                       websocket=self._websockets)

        chat_graph = chat_agent.create_graph()
        chat_graph = chat_graph.with_config({'callbacks': [get_langfuse_callback()], "run_name": 'Chatbot chat chain'})

        return chat_graph

    async def achat(self, c_input: ChatbotInput):
        r = await self.achat_stream(c_input)
        return r

    async def achat_stream(self, c_input: ChatbotInput):
        # Prepare dataset
        scenario_db_type: ChatScenarioDBType = ChatScenarioDBType(**self.chatroom_db.get_scenario_info(scenario_id=1))
        chatroom_db_type: ChatRoomDBType = self.chatroom_db.get_chatroom_id(user_id=c_input.user_id,
                                                                            scenario_id=scenario_db_type.id,
                                                                            session_id=c_input.session_id)

        all_chatbot_ids = scenario_db_type.chatbot_id.copy()
        all_chatbot_ids.append(scenario_db_type.narrator_id)
        all_chatbot_npc = await self.npc_db.get_bots(all_chatbot_ids)

        chat_graph = self.get_chat_graph(c_input, scenario_db_type, all_chatbot_npc, chatroom_db_type)

        result = await chat_graph.ainvoke({'query': c_input.text, 'scenario': scenario_db_type.background})

        bot_message: list[StreamingDataChunkType] = result['final_message']

        messages = self._save_message_to_db(c_input, chatroom_db_type, bot_message)
        self.chatbot_message_db.update_summary(chatroom_db_type.id, result['new_chatroom_summary'])
        self._memory.queue_message(scenario_db_type, chatroom_db_type, messages)

        return result

    # * DB Operation
    def _save_message_to_db(self, c_input: ChatbotInput, chatroom_db: ChatRoomDBType,
                            bot_messages: list[StreamingDataChunkType]):

        bot_message_db_inputs: list[ChatMessageDBInputType] = []
        for m in bot_messages:
            bot_message_db_inputs.append(
                ChatMessageDBInputType(
                    chatroom_id=chatroom_db.id, body=m.data,
                    message_type=m.identity,
                    bubble_id=m.bubble_id, user_id=m.source_id
                )
            )

        insert_messages_data = [
            ChatMessageDBInputType(
                chatroom_id=chatroom_db.id, body=c_input.text,
                message_type=ChatbotUserEnum.human,
                bubble_id=str(uuid.uuid4()), user_id=c_input.user_id
            ), *bot_message_db_inputs
        ]

        # insert user
        self.chatbot_message_db.insert_message(insert_messages_data)

        return insert_messages_data
