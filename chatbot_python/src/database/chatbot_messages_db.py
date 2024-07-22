import psycopg
from psycopg.rows import dict_row

from database.db_manager import get_conn_uri
from model.chatbot_model import ChatbotUserEnum

class ChatbotMessagesDB():
    Table = 'chatbot_messages'

    async def insert_message(self, chatroom_id: int, body: str, message_type: ChatbotUserEnum,
                             bubble_id: str, chatbot_id: int = -1):
        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""INSERT INTO {self.Table}(chatbot_id, chatroom_id, bubble_id, message_type, body)
                                VALUES(%s, %s, %s, %s, %s)""",
                            (chatbot_id, chatroom_id, bubble_id, message_type, body))
            conn.commit()
