from uuid import uuid4
from typing import List
from question_generator import generate_questions

def create_quiz(subject: str, question_count: int, option_count: int):
    print('Generating quiz questions...')
    try:
        generated_questions = generate_questions(
            subject=subject, question_count=question_count, option_count=option_count)
    except Exception as err:
        print('Error generating questions:', err, sep='\n')
        return

    quiz_id = uuid4().hex  # TODO: Create quiz and get its id
    questions = []
    question_options = []


