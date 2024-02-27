from app import app, db
from app.models import Question
from flask import request
from sqlalchemy.sql.expression import func


@app.get('/questions')
def get_all_questions():
    return [question.to_dict() for question in Question.query.all()]


@app.get('/quizzes/<int:quiz_id>/questions')
def get_quiz_questions(quiz_id: int):
    return [question.to_dict() for question in Question.query.filter_by(quiz_id=quiz_id).order_by(func.random()).all()]


@app.delete('/questions')
def delete_all_questions():
    Question.query.delete()
    db.session.commit()
    return '', 204
