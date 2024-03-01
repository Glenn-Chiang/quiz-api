from flask import request, jsonify
from app import app, db
from app.models import Quiz, Question, Choice
from app.routes.errors import error_response
from quiz_generator.question_generator import generate_questions
from sqlalchemy import select


@app.get('/quizzes/<int:quiz_id>')
def get_quiz(quiz_id: int):
    return Quiz.query.get_or_404(ident=quiz_id).to_dict()


@app.get('/quizzes')
def get_quizzes():
    page = request.args.get('page', 1, type=int)
    # default 10 per page, maximum 100 per page
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Quiz.to_collection_dict(select(Quiz), page=page, per_page=per_page, endpoint='get_quizzes')


MIN_QUESTIONS = 5
MAX_QUESTIONS = 20
MIN_CHOICES = 2
MAX_CHOICES = 6


@app.post('/quizzes')
def create_quiz():
    quiz_data = request.get_json()
    for field in ['subject', 'question_count', 'choice_count']:
        if field not in quiz_data:
            return error_response(status_code=400, message=f"'{field}' field is required")

    subject = quiz_data['subject']
    creator_id = quiz_data.get('creator_id', None)

    try:
        creator_id = int(creator_id) if creator_id else None
        question_count = int(quiz_data['question_count'])
        choice_count = int(quiz_data['choice_count'])

        # Limit the question_count and choice_count that can be requested
        if question_count < MIN_QUESTIONS or question_count > MAX_QUESTIONS:
            return error_response(status_code=400, message=f"Allowed range for question_count: {MIN_QUESTIONS} - {MAX_QUESTIONS}")
        if choice_count < MIN_QUESTIONS or choice_count > MAX_CHOICES:
            return error_response(status_code=400, message=f"Allowed range for choice_count: {MIN_CHOICES} - {MAX_CHOICES}")

    except ValueError:
        return error_response(status_code=400, message=f"question_count, choice_count and creator_id must be integers")

    quiz = Quiz(subject=subject, creator_id=creator_id)
    db.session.add(quiz)
    db.session.flush()

    try:
        questions_with_choices = generate_questions(
            subject=subject, question_count=question_count, choice_count=choice_count)
    except Exception as error:
        return error_response(status_code=500, message=f"Error generating questions: {error}")

    for question_data in questions_with_choices:
        question = Question(text=question_data['question'], quiz_id=quiz.id)
        db.session.add(question)
        db.session.flush()

        choices = [Choice(text=choice['text'], correct=choice['correct'],
                          question_id=question.id) for choice in question_data['choices']]
        db.session.bulk_save_objects(choices)

    db.session.commit()

    return quiz.to_dict(), 201


@app.delete('/quizzes/<int:quiz_id>')
def delete_quiz(quiz_id: int):
    quiz = Quiz.query.filter(Quiz.id == quiz_id).first_or_404()
    db.session.delete(quiz)
    db.session.commit()
    return '', 204


@app.delete('/quizzes')
def delete_all_quizzes():
    Quiz.query.delete()
    db.session.commit()
    return '', 204
