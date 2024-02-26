from app import app
from app.models import Question

@app.get('/questions')
def get_all_questions():
    return [question.to_dict() for question in Question.query.all()]

@app.get('/quizzes/<int:quiz_id>/questions')
def get_quiz_questions(quiz_id: int):
    return [question.to_dict() for question in Question.query.filter_by(quiz_id=quiz_id).all()]

