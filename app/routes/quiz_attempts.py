from app import app, db
from app.models import QuizAttempt
from flask import request
from app.routes.errors import error_response

@app.get('/attempts')
def get_all_attempts():
    return [attempt.to_dict() for attempt in QuizAttempt.query.all()]


@app.get('/attempts/<int:attempt_id>')
def get_attempt_by_id(attempt_id: int):
    return QuizAttempt.query.get_or_404(ident=attempt_id).to_dict()


@app.get('/quizzes/<int:quiz_id>/attempts')
def get_quiz_attempts(quiz_id: int):
    return [attempt.to_dict() for attempt in QuizAttempt.query.filter(QuizAttempt.quiz_id == quiz_id).all()]


@app.get('/users/<int:user_id>/attempts')
def get_user_attempts(user_id: int):
    return [attempt.to_dict() for attempt in QuizAttempt.query.filter(QuizAttempt.user_id == user_id).all()]


@app.post('/quizzes/<int:quiz_id>/attempts')
def add_quiz_attempt(quiz_id: int):
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return error_response(status_code=400, message='Invalid or missing user_id')
    
    quiz_attempt = QuizAttempt(quiz_id=quiz_id, user_id=user_id)
    db.session.add(quiz_attempt)
    db.session.commit()

    return quiz_attempt.to_dict(), 201