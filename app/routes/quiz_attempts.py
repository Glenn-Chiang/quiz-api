from app import app
from app.models import QuizAttempt


@app.get('/attempts')
def get_all_attempts():
    return [attempt.to_dict() for attempt in QuizAttempt.query.all()]


@app.get('/attempts/<int:attempt_id>')
def get_attempt_by_id(quiz_id: int):
    return QuizAttempt.query.get_or_404(ident=quiz_id).to_dict()


@app.get('/quizzes/<int:quiz_id>/attempts')
def get_quiz_attempts(quiz_id: int):
    return [attempt.to_dict() for attempt in QuizAttempt.query.filter(QuizAttempt.quiz_id == quiz_id).all()]


@app.get('/users/<int:user_id>/attempts')
def get_user_attempts(user_id: int):
    return [attempt.to_dict() for attempt in QuizAttempt.query.filter(QuizAttempt.user_id == user_id).all()]
