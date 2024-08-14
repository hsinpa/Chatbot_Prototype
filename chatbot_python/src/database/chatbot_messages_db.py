import psycopg
from psycopg.rows import dict_row

from database.db_manager import get_conn_uri
from model.chatbot_model import ChatbotUserEnum, ChatMessageDBInputType


class ChatbotMessagesDB:
    Table = 'chatbot_messages'

    def get_messages(self, user_id: str, session_id: str):
        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT chatbot_messages.user_id as user_id, chatbot_messages.id as message_id, 
                bubble_id, body, message_type 
                FROM {self.Table}
                LEFT JOIN chatroom on chatroom.id=chatbot_messages.chatroom_id
                WHERE chatroom.session_id=%s and chatroom.user_id=%s""", (session_id, user_id))

                fetch_r = cur.fetchall()
                return fetch_r


    def insert_message(self, message_inputs: list[ChatMessageDBInputType]):
        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                for message in message_inputs:
                    cur.execute(f"""INSERT INTO {self.Table}(user_id, chatroom_id, bubble_id, message_type, body)
                                    VALUES(%s, %s, %s, %s, %s)""",
                                (message.user_id, message.chatroom_id, message.bubble_id,
                                 message.message_type.value, message.body))
            conn.commit()

    def update_summary(self, chatroom_id: int, summary: str):
        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""UPDATE chatroom SET summary = %s WHERE id = %s""",
                            (summary, chatroom_id))
            conn.commit()
