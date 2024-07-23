import psycopg
from psycopg.rows import dict_row

from database.db_manager import get_conn_uri


class ChatRoomDB:
    Chatroom_Table = 'chatroom'
    Chatbot_Table = 'chatbot_messages'

    async def get_chatroom_info(chatroom_id: int):

        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                pass
                # cur.execute(f"""SELECT id, chatbot_id, narrator_id, """,
