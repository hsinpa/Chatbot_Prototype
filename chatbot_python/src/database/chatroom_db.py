import psycopg
from psycopg.rows import dict_row

from database.db_manager import get_conn_uri


class ChatRoomDB:
    Chatroom_Table = 'chatroom'
    Chatbot_Table = 'chatbot_messages'

    async def get_chatroom_info(scenario_id: int):

        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                scenario_fetch = cur.execute("""SELECT id, chatbot_id, narrator_id,
                scenario_name, background FROM room_scenario WHERE id=%s""", (scenario_id,))

