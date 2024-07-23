CREATE TABLE IF NOT EXISTS bot (
    id varchar(255) PRIMARY KEY,
    name varchar(255),
    personality text,
    instruction text,
    background_story text,
    type varchar(64),
    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS chatroom (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    chatbot_id varchar(255)[],
    narrator_id varchar(255),
    session_id varchar(255),
    user_id text,
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY(narrator_id) REFERENCES bot(id)
);
CREATE INDEX chatroom_session_index ON chatroom (session_id);

CREATE TABLE IF NOT EXISTS chatbot_messages (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id varchar(255),
    chatroom_id int,
    bubble_id text,
    message_type varchar(32),
    body text,
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY(chatroom_id) REFERENCES chatroom(id)
);

CREATE TABLE IF NOT EXISTS chatroom_summary (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    chatroom_id int,
    session_id varchar(255),
    user_id text,
    summary text,
    updated_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY(chatroom_id) REFERENCES chatroom(id)
);
CREATE INDEX chatbot_summary_index ON chatroom_summary (session_id);
