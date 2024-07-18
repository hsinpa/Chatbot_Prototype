import json
import uuid
from typing import AsyncIterator

from langchain_core.runnables import Runnable
from langchain_core.runnables.utils import Output

from agent.chatbot.chatbot_type import StreamingDataChunkType, DataChunkType
from websocket.socket_static import SocketEvent
from websocket.websocket_manager import WebSocketManager


async def streaming_exec(websockets: WebSocketManager, session_id: str, token: str,
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
                                             type=DataChunkType.Chunk)

        json_string = {'event': SocketEvent.bot, **stream_data.model_dump()}
        await websockets.send(session_id=session_id, data=json.dumps(json_string))
        results = results + data_chunk
        index += 1
    return results
