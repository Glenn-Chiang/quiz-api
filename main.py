from app import app, db
import sqlalchemy
import sqlalchemy.orm

@app.shell_context_processor
def make_shell_context():
    return {'sqlalchemy': sqlalchemy, 'orm': sqlalchemy.orm}