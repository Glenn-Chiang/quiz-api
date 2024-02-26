from app import app, db
from app.models import Choice

@app.get('/choices')
def get_all_choices():
    return [choice.to_dict() for choice in Choice.query.all()]

@app.get('/questions/<int:question_id>/choices')
def get_question_choices(question_id: int):
    return [choice.to_dict() for choice in Choice.query.filter_by(question_id=question_id).all()]

@app.delete('/choices')
def delete_all_choices():
    Choice.query.delete()
    db.session.commit()
    return '', 204