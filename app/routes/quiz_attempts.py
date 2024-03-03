from app import app, db
from app.models import QuizAttempt
from flask import request
from app.routes.errors import error_response
from sqlalchemy import select


@app.get('/attempts')
def get_all_attempts():
    return [attempt.to_dict() for attempt in QuizAttempt.query.all()]


@app.get('/attempts/<int:attempt_id>')
def get_attempt_by_id(attempt_id: int):
    return QuizAttempt.query.get_or_404(ident=attempt_id).to_dict()


@app.get('/quizzes/<int:quiz_id>/attempts')
def get_quiz_attempts(quiz_id: int):
    return [attempt.to_dict() for attempt in QuizAttempt.query.filter(QuizAttempt.quiz_id == quiz_id).all()]


# Get all quiz attempts made by this user
@app.get('/users/<int:user_id>/attempts')
def get_user_attempts(user_id: int):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    return QuizAttempt.to_collection_dict(select(QuizAttempt).where(QuizAttempt.user_id == user_id),
                                          page=page, per_page=per_page,
                                          endpoint='get_user_attempts', user_id=user_id)


# Should be called when a user starts to attempt a quiz
@app.post('/quizzes/<int:quiz_id>/attempts')
def add_quiz_attempt(quiz_id: int):
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return error_response(status_code=400, message='Missing or invalid user_id')

    quiz_attempt = QuizAttempt(quiz_id=quiz_id, user_id=user_id)
    db.session.add(quiz_attempt)
    db.session.commit()

    return quiz_attempt.to_dict(), 201
