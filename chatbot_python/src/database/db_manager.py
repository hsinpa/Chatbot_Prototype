import os
import uuid

from psycopg.rows import dict_row
import psycopg
from database.bot_chat_sql import BOT_NAME, BOT_PERSONALITY, BOT_INSTRUCTION, BOT_BACKGROUND, BOT_TYPE, SCENARIO_NAME, \
    SCENARIO_BACKGROUND
from database.bot_narrator_sql import NARRATOR_NAME, NARRATOR_PERSONALITY, NARRATOR_INSTRUCTION, NARRATOR_BACKGROUND, \
    NARRATOR_TYPE

def get_conn_uri():
    user_id = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    postgres_db = os.environ['POSTGRES_DB']
    postgres_host = os.environ['POSTGRES_HOST']

    conn_str = f"host={postgres_host} port=5432 dbname={postgres_db} user={user_id} password={password} connect_timeout=10"
    return conn_str

class PostgresDB_Chat():
    def __init__(self):
        self.create_init_table()

    def create_init_table(self):
        conn_str = get_conn_uri()

        with psycopg.connect(conn_str, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Execute a command: this creates a new table
                cur.execute(f"""SELECT COUNT(id) as c FROM bot WHERE name='{NARRATOR_NAME}'""")
                narrator_fetch = cur.fetchone()

                cur.execute(f"""SELECT COUNT(id) as c FROM bot WHERE name='{BOT_NAME}'""")
                bot_fetch = cur.fetchone()

                cur.execute(f"""SELECT COUNT(id) as c FROM room_scenario WHERE id=1""")
                room_scenario_fetch = cur.fetchone()

                print('room_scenario_fetch', room_scenario_fetch)

                chatbot_id = str(uuid.uuid4())
                narrator_id = str(uuid.uuid4())

                if narrator_fetch['c'] == 0:
                    cur.execute(f"""INSERT INTO bot(id, name, personality, instruction, background_story, type)
                                    VALUES(%s, %s, %s, %s, %s, %s)""",
                                (chatbot_id, NARRATOR_NAME, NARRATOR_PERSONALITY, NARRATOR_INSTRUCTION,
                                 NARRATOR_BACKGROUND, NARRATOR_TYPE))

                if bot_fetch['c'] == 0:
                    cur.execute(f"""INSERT INTO bot(id, name, personality, instruction, background_story, type)
                                    VALUES(%s, %s, %s, %s, %s, %s)""",
                                (narrator_id, BOT_NAME, BOT_PERSONALITY, BOT_INSTRUCTION,
                                 BOT_BACKGROUND, BOT_TYPE))

                if room_scenario_fetch['c'] == 0:
                    cur.execute(f"""INSERT INTO room_scenario(chatbot_id, narrator_id, scenario_name, background)
                                    VALUES(%s, %s, %s, %s)""",
                                ([chatbot_id], narrator_id, SCENARIO_NAME, SCENARIO_BACKGROUND))

                conn.commit()
