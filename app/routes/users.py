from flask import request
from app import app, db
from app.models import User
from app.routes.errors import error_response
from sqlalchemy.exc import IntegrityError

@app.get('/users')
def get_users():
    return [user.to_dict() for user in User.query.all()]


@app.get('/users/<int:user_id>')
def get_user(user_id):
    return User.query.get_or_404(ident=user_id).to_dict()


@app.post('/users')
def create_user():
    user_data: dict = request.get_json()

    username = user_data.get('username', None)
    user_id = user_data.get('id', None)
    
    if not username:
        return error_response(status_code=400, message='username is required')
    
    # Allow the client to optionally provide the user id
    if user_id:
        try:
            user_id = int(user_id)
        except ValueError:
            return error_response(status_code=400, message='user id must be an integer')

    try:
        user = User(username=username, id=user_id)
        db.session.add(user)
        db.session.commit()
    except IntegrityError as error:
        return error_response(status_code=409, message=f'username or user_id is already in use')

    return user.to_dict(), 201
