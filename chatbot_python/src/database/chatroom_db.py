import psycopg
from psycopg import AsyncConnection
from psycopg.rows import dict_row

from database.db_manager import get_conn_uri
from model.chatbot_model import ChatRoomDBType


class ChatRoomDB:
    Scenario_Table = 'room_scenario'
    Chatroom_Table = 'chatroom'
    Chatbot_Table = 'chatbot_messages'

    def get_scenario_info(self, scenario_id: int):

        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""SELECT id, chatbot_id, narrator_id, scenario_name, background FROM {self.Scenario_Table} WHERE id=%s""",
                    (scenario_id,))

                return cur.fetchone()

    def get_chatroom_id(self, user_id: str, session_id: str, scenario_id: int) -> ChatRoomDBType:
        with psycopg.connect(get_conn_uri(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""SELECT id, session_id, scenario_id, user_id, summary, created_date
                    FROM {self.Chatroom_Table} WHERE session_id=%s AND scenario_id=%s AND user_id=%s""",
                    (session_id, scenario_id, user_id))

                chatroom_fetch_r = cur.fetchone()

                if chatroom_fetch_r is not None:
                    return ChatRoomDBType(**chatroom_fetch_r)

                # If not exist, insert a new one
                cur.execute(
                    f"""INSERT INTO {self.Chatroom_Table}(session_id, scenario_id, user_id)
                     VALUES(%s, %s, %s) RETURNING id, session_id, scenario_id, user_id, summary, created_date""",
                    (session_id, scenario_id, user_id))

                id_of_new_row = cur.fetchone()
                conn.commit()

                return ChatRoomDBType(**id_of_new_row)