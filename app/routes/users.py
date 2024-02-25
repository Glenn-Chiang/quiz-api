from flask import jsonify, request
from app import app, db
from app.models import User


@app.get('/users')
def get_users():
    users = User.query.all()
    return jsonify(users)


@app.get('/users/<int:user_id>')
def get_user(user_id):
    return User.query.get_or_404(ident=user_id)

@app.post('/users')
def create_user():
    pass