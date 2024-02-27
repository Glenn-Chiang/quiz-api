from app import app
from app.models import UserChoice, Choice


@app.get('/user_choices')
def get_all_user_choices():
    return [user_choice.to_dict() for user_choice in UserChoice.query.all()]


@app.get('/attempts/<int:attempt_id>/user_choices')
def get_user_choices_for_attempt(attempt_id: int):
    return [user_choice.to_dict() for user_choice in UserChoice.query.filter(UserChoice.attempt_id == attempt_id).all()]


@app.get('/questions/<int:question_id>/user_choices')
def get_user_choices_for_question(question_id: int):
    return [user_choice.to_dict() for user_choice in UserChoice.query
            .join(Choice, Choice.id == UserChoice.choice_id)
            .filter(Choice.question_id == question_id).all()]


@app.get('/choices/<int:choice_id>/user_choices')
def get_user_choices_for_choice(choice_id: int):
    return [user_choice.to_dict() for user_choice in UserChoice.query.filter(UserChoice.choice_id == choice_id).all()]
