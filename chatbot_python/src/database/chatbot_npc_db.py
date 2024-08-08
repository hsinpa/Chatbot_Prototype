import asyncio
from typing import List

from pydantic import TypeAdapter

from database.db_manager import FetchType, async_db_ops, sync_db_ops
from model.chatbot_model import ChatbotNPCDBType


class ChatbotNpcDB:
    Table = 'bot'

    async def get_bots(self, bot_ids: list[str]) -> List[ChatbotNPCDBType]:

        list_sql_cmd = ''
        for index, bot_id in enumerate(bot_ids):
            if index > 0:
                list_sql_cmd += ' OR '

            list_sql_cmd += f"id='{bot_id}'"

        sql_syntax = f"SELECT * FROM {self.Table} WHERE {list_sql_cmd}  ORDER BY type"

        fetch_array = sync_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Many)
        print(fetch_array)
        ta = TypeAdapter(List[ChatbotNPCDBType])
        return ta.validate_python(fetch_array)
