from flask import request
from app import app, db
from app.models import Quiz
from app.routes.errors import error_response
from quiz_generator.quiz_generator import generate_quiz


@app.get('/quizzes')
def get_quizzes():
    return [quiz.to_dict() for quiz in Quiz.query.all()]


@app.get('/quizzes/<int:quiz_id>')
def get_quiz(quiz_id: int):
    return Quiz.query.get_or_404(ident=quiz_id).to_dict()


@app.post('/quizzes')
def create_quiz():
    quiz_data = request.get_json()
    for field in ['subject', 'creator_id', 'question_count', 'choice_count']:
        if field not in quiz_data:
            return error_response(status_code=400, message=f'"{field}" field is required')

    subject = quiz_data['subject']
    creator_id = quiz_data['creator_id']

    try:
        question_count = int(quiz_data['question_count'])
        choice_count = int(quiz_data['choice_count'])
    except ValueError:
        return error_response(status_code=400, message=f"'question_count' and 'choice_count' must be integers")

    quiz = Quiz(subject=subject, creator_id=creator_id)
    db.session.add(quiz)
    db.session.commit()
    db.session.refresh(quiz)

    quiz = generate_quiz(subject=subject, question_count=question_count, choice_count=choice_count)
    # TODO: Add quiz questions and choices to corresponding tables