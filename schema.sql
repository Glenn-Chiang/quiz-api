CREATE TABLE quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    subject TEXT NOT NULL
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE question (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    quiz_id INTEGER NOT NULL
    text TEXT NOT NULL
    FOREIGN KEY (quiz_id) REFERENCES quiz (id)
)

CREATE TABLE question_option (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    quiz_id INTEGER NOT NULL
    question_id INTEGER NOT NULL
    text TEXT NOT NULL
    is_correct INTEGER NOT NULL
    FOREIGN KEY (quiz_id) REFERENCES quiz (id)
    FOREIGN KEY (question_id) REFERENCES question (id)
)