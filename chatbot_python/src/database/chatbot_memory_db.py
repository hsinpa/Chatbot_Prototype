from database.db_manager import async_db_ops, FetchType


class ChatbotMemoryDB:
    Table = 'chatbot_memory'

    async def get_by_session_id(self, session_id: str):
        sql_syntax = f"SELECT * FROM {self.Table} WHERE session_id = %s"
        return await async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Many, parameters=[session_id])

    async def create_memory(self, session_id: str, attribute: str, body: str):
        sql_syntax = f"INSERT INTO {self.Table} (attribute, body, session_id) VALUES(%s, %s, %s) RETURNING id"
        return await async_db_ops(sql_syntax=sql_syntax, parameters=[attribute, body, session_id])

    async def update_memory(self, memory_id: int, attribute: str, body: str):
        sql_syntax = f"UPDATE {self.Table} SET attribute=%s, body=%s WHERE id=%s"
        return await async_db_ops(sql_syntax=sql_syntax, parameters=[attribute, body, memory_id])

    async def delete_memory(self, memory_id: id):
        sql_syntax = f"DELETE FROM {self.Table} WHERE id=%s"
        return await async_db_ops(sql_syntax=sql_syntax, parameters=[memory_id])