from app import app

@app.get('/quizzes')
def get_quizzes():
    return 'quizzes'

@app.get('/quizzes/<quiz_id>')
def get_quiz(quiz_id: str):
    return f'Quiz: {quiz_id}'