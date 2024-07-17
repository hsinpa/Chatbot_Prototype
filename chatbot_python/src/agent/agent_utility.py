import json
from typing import AsyncIterator

from langchain_core.runnables import Runnable
from langchain_core.runnables.utils import Output

from agent.chatbot.chatbot_type import StreamingDataChunkType, DataChunkType
from websocket.socket_static import SocketEvent
from websocket.websocket_manager import WebSocketManager


async def streaming_exec(websockets: WebSocketManager, session_id: str, stream: AsyncIterator[Output]):
    results = ''

    async for chunk in stream:
        data_chunk = str(chunk)
        stream_data = StreamingDataChunkType(session_id=session_id, data=data_chunk, token='', type=DataChunkType.Chunk)
        json_string = {'event': SocketEvent.bot, **stream_data.model_dump()}
        await websockets.send(session_id=session_id, data=json.dumps(json_string))
        results = results + data_chunk

    return results
