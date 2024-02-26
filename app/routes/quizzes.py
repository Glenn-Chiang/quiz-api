from flask import request, jsonify
from app import app, db
from app.models import Quiz, Question, Choice
from app.routes.errors import error_response
from quiz_generator.question_generator import generate_questions


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
