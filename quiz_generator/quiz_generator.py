from uuid import uuid4
from typing import List
from question_generator import generate_questions


def generate_quiz(subject: str, question_count: int, choice_count: int):
    print('Generating quiz questions...')
    try:
        generated_questions = generate_questions(
            subject=subject, question_count=question_count, choice_count=choice_count)
    except Exception as err:
        print('Error generating questions:', err, sep='\n')
        return

    
