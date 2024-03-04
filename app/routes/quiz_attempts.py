from app import app, db
from app.models import QuizAttempt, AttemptQuestion, UserChoice
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


# Get questions done on given attempt
@app.get('/attempts/<int:attempt_id>/questions')
def get_attempt_questions(attempt_id: int):
    return [question.to_dict() for question in AttemptQuestion.query.filter(AttemptQuestion.attempt_id == attempt_id).order_by(AttemptQuestion.sequence_number).all()]


# Get all quiz attempts made by given user, sorted from most recent to least recent
@app.get('/users/<int:user_id>/attempts')
def get_user_attempts(user_id: int):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    return QuizAttempt.to_collection_dict(select(QuizAttempt).where(QuizAttempt.user_id == user_id).order_by(QuizAttempt.timestamp.desc()),
                                          page=page, per_page=per_page,
                                          endpoint='get_user_attempts', user_id=user_id)


# Save a new quiz attempt with the sequence of questions given and the choices chosen by the user
@app.post('/quizzes/<int:quiz_id>/attempts')
def add_quiz_attempt(quiz_id: int):
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return error_response(status_code=400, message='Missing or invalid user_id')

    attempt_data = request.get_json()
    questions_with_choice = attempt_data['questions']

    # Create new quiz attempt
    quiz_attempt = QuizAttempt(quiz_id=quiz_id, user_id=user_id)
    db.session.add(quiz_attempt)
    db.session.flush()

    attempt_questions = [AttemptQuestion(attempt_id=quiz_attempt.id, question_id=question['question_id'],
                                         sequence_number=index) for index, question in enumerate(questions_with_choice)]
    user_choices = [UserChoice(attempt_id=quiz_attempt.id, choice_id=question['choice_id'])
                    for question in questions_with_choice]

    db.session.bulk_save_objects(attempt_questions)
    db.session.bulk_save_objects(user_choices)

    db.session.commit()

    return quiz_attempt.to_dict(), 201
