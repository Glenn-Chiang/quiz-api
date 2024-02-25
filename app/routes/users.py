from flask import jsonify, request
from app import app, db
from app.models import User


@app.get('/users')
def get_users():
    return [user.to_dict() for user in User.query.all()]


@app.get('/users/<int:user_id>')
def get_user(user_id):
    return User.query.get_or_404(ident=user_id).to_dict()

@app.post('/users')
def create_user():
    user_data = request.get_json()
    if 'username' not in user_data:
        #TODO: Handle missing username
        ...
    username = user_data['username']
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
