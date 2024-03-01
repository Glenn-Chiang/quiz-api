from app import app, db
from app.models import Question
from flask import request
from sqlalchemy.sql.expression import func
from sqlalchemy import select


@app.get('/questions')
def get_all_questions():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    return Question.to_collection_dict(select(Question), page=page, per_page=per_page, endpoint='get_quizzes')


@app.get('/quizzes/<int:quiz_id>/questions')
def get_quiz_questions(quiz_id: int):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    return Question.to_collection_dict(select(Question).where(Question.quiz_id == quiz_id).order_by(func.random()),
                                       page=page, per_page=per_page, endpoint='get_quiz_questions', quiz_id=quiz_id)


@app.delete('/questions')
def delete_all_questions():
    Question.query.delete()
    db.session.commit()
    return '', 204
