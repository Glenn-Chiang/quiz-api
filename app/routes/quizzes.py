from app import app
from app.models import Quiz

@app.get('/quizzes')
def get_quizzes():
    return [quiz.to_dict() for quiz in Quiz.query.all()]

@app.get('/quizzes/<int:quiz_id>')
def get_quiz(quiz_id: int):
    return Quiz.query.get_or_404(ident=quiz_id).to_dict() 