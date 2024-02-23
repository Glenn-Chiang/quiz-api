import sqlite3

def get_db():
    db = sqlite3.connect('data.db')
    db.row_factory = sqlite3.Row
    return db

# Create tables from schema
def init_db():
    db = get_db()
    cursor = db.cursor()

    with open('schema.sql', 'r') as file:
        cursor.executescript(file.read())

    db.commit()
    db.close()


def execute_query(query: str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()
