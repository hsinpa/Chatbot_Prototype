CREATE TABLE IF NOT EXISTS bot (
    id varchar(255) PRIMARY KEY,
    name varchar(255),
    personality text,
    instruction text,
    background_story text,
    type varchar(64),
    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS room_scenario (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    chatbot_id varchar(255)[],
    narrator_id varchar(255),
    scenario_name text,
    background text,
    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS chatroom (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id varchar(255),
    scenario_id int,
    user_id text,
    summary text NOT NULL DEFAULT '',
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY(scenario_id) REFERENCES room_scenario(id)
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

CREATE TABLE IF NOT EXISTS chatbot_memory (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    body text,
    attribute varchar(255),
    session_id varchar(255),
    user_id varchar(255),
    created_date DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE INDEX memory_session_index ON chatbot_memory (session_id);
CREATE INDEX memory_user_index ON chatbot_memory (user_id);
