from app import app


@app.get('/users')
def get_users():
    return 'users'


@app.get('/users/<user_id>')
def get_user(user_id: str):
    return f'User: {user_id}'
