from flask import jsonify, request
from app import app, db
from app.models import User
from app.routes.errors import error_response


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
        return error_response(status_code=400, message='username is required')

    username = user_data['username']

    if User.query.filter_by(username=username).first():
        return error_response(status_code=409, message='username is already in use')

    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    return user.to_dict(), 201
