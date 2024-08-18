import json
import uuid
from datetime import datetime, timezone
from typing import AsyncIterator, Any

from langchain_core.messages import MessageLikeRepresentation
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.utils import Output

from agent.chatbot.chatbot_type import StreamingDataChunkType, DataChunkType
from agent.memory.memory_type import ChatKnowledgeType, Category
from model.chatbot_model import ChatMessageDBInputType, ChatbotUserEnum, ChatbotNPCDBType
from websocket.socket_static import SocketEvent
from websocket.websocket_manager import WebSocketManager


async def streaming_exec(websockets: WebSocketManager, websocket_id: str, session_id: str, token: str,
                         bot_id: str, identity: ChatbotUserEnum,
                         stream: AsyncIterator[Output]):
    results = ''
    bubble_id = str(uuid.uuid4())
    index = 0
    async for chunk in stream:
        data_chunk = str(chunk)

        stream_data = StreamingDataChunkType(session_id=session_id,
                                             data=data_chunk,
                                             token=token,
                                             bubble_id=bubble_id,
                                             index=index,
                                             source_id=bot_id,
                                             time=datetime.now(timezone.utc).timestamp(),
                                             identity=identity,
                                             type=DataChunkType.Chunk)

        json_string = {'event': SocketEvent.bot, **stream_data.model_dump()}
        await websockets.send(socket_id=websocket_id, data=json.dumps(json_string))
        results = results + data_chunk
        index += 1

    full_stream_data = StreamingDataChunkType(session_id=session_id,
                                              data=results,
                                              token=token,
                                              bubble_id=bubble_id,
                                              index=index,
                                              source_id=bot_id,
                                              identity=identity,
                                              time=datetime.now(timezone.utc).timestamp(),
                                              type=DataChunkType.Complete)

    full_stream_data.type = DataChunkType.Complete
    full_stream_data.data = results

    return full_stream_data


def reform_db_message(messages: list[ChatMessageDBInputType]):
    messages_output: list[MessageLikeRepresentation] = []

    for m in messages:
        messages_output.append(('human' if m.message_type != ChatbotUserEnum.human else 'ai', m.body))

    return messages_output


def db_message_to_str(messages: list[ChatMessageDBInputType]):
    message_str = ''
    for m in messages:
        message_str += f'Message from {m.message_type.value}: \n{m.body}'

    return message_str


def db_message_to_prompt(system_prompt: str, human_prompt: str,
                         messages: list[ChatMessageDBInputType]) -> ChatPromptTemplate:
    agent_message = [('system', system_prompt)]

    # Ignore narrator
    for message in messages:
        if message.message_type == ChatbotUserEnum.human:
            agent_message.extend([('user', message.body)])

        if message.message_type == ChatbotUserEnum.bot:
            agent_message.extend([('ai', message.body)])

    agent_message.append(('user', human_prompt))

    prompt_template = ChatPromptTemplate(agent_message)
    return prompt_template


def db_memory_to_str(memories: list[ChatKnowledgeType]):
    if memories is None or len(memories) <= 0:
        return 'Empty'

    knowledge_memo_str = 'Knowledge from user: \n'
    item_memo_str = '\nItem hold by user: \n'

    for m in memories:
        if m.attribute.value == Category.Knowledge:
            knowledge_memo_str += f'ID [{m.knowledge_id}]: {m.knowledge}\n'

        if m.attribute.value == Category.Item:
            item_memo_str += f'ID [{m.knowledge_id}]: {m.knowledge}\n'

    return knowledge_memo_str + item_memo_str


def bot_variable(chatbot: ChatbotNPCDBType, summary: str):
    return {
        'name': chatbot.name,
        'personality': chatbot.personality,
        'background': chatbot.background_story,
        'goal': chatbot.instruction,
        'summary': summary,
    }
