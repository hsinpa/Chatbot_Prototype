import psycopg
from psycopg.rows import dict_row

from database.db_manager import get_conn_uri
from model.chatbot_model import ChatbotUserEnum, ChatMessageDBInputType


class ChatbotMessagesDB:
    Table = 'chatbot_messages'

    async def insert_message(self, message_inputs: list[ChatMessageDBInputType]):

        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                for message in message_inputs:
                    cur.execute(f"""INSERT INTO {self.Table}(user_id, chatroom_id, bubble_id, message_type, body)
                                    VALUES(%s, %s, %s, %s, %s)""",
                                (message.user_id, message.chatroom_id, message.bubble_id,
                                 message.message_type.value, message.body))
            conn.commit()
