import asyncio
from asyncio import AbstractEventLoop
from typing import Callable, Awaitable, List

from pydantic.v1 import parse_obj_as

from agent.memory.memory_agent import MemoryGraphAgent
from agent.memory.memory_type import ChatKnowledgeOpsType, Action, ChatKnowledgeType
from database.chatbot_memory_db import ChatbotMemoryDB
from model.chatbot_model import ChatScenarioDBType, ChatRoomDBType, ChatMessageDBInputType
from threading import Thread

from utility.utility_method import get_langfuse_callback


class MemoryManager:

    def __init__(self):
        self._memory_db: ChatbotMemoryDB = ChatbotMemoryDB()
        pass

    def queue_message(self, scenario: ChatScenarioDBType, chatroom_info: ChatRoomDBType,
                      q_message: list[ChatMessageDBInputType]):
        new_loop = asyncio.new_event_loop()  # Create a new event loop

        t = Thread(target=self._run_async_func, args=(self._start_memory_work, new_loop, scenario,
                                                      chatroom_info, q_message))
        t.start()

    def _run_async_func(self, callback: Callable[..., Awaitable[None]], loop: AbstractEventLoop, *kargs):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(callback(*kargs))

    async def _process_memory_db(self, session_id: str, knowledge_types: list[ChatKnowledgeOpsType]):
        if knowledge_types is None:
            return

        for knowledge_type in knowledge_types:
            if knowledge_type.action == Action.Create:
                await self._memory_db.create_memory(session_id, knowledge_type.attribute, knowledge_type.knowledge)

            if knowledge_type.action == Action.Update:
                await self._memory_db.update_memory(knowledge_type.knowledge_id, knowledge_type.attribute,
                                                    knowledge_type.knowledge)

            if knowledge_type.action == Action.Delete:
                await self._memory_db.delete_memory(knowledge_type.knowledge_id)

    async def _start_memory_work(self, scenario: ChatScenarioDBType, chatroom_info: ChatRoomDBType,
                                 q_message: list[ChatMessageDBInputType]):

        memory_dict = await self._memory_db.get_by_session_id(chatroom_info.session_id)
        memory_knowledge = parse_obj_as(List[ChatKnowledgeType], memory_dict)

        memory_agent = MemoryGraphAgent(chatroom_info.id, q_message, memory_knowledge)
        memory_graph = memory_agent.create_graph().with_config({
            "run_name": 'Memory Ops', 'callbacks': [get_langfuse_callback()]})

        knowledge_types = await memory_graph.ainvoke({'messages': q_message})
        await self._process_memory_db(chatroom_info.session_id, knowledge_types['knowledge_ops'])
