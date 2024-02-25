from uuid import uuid4
from typing import List
from question_generator import generate_questions


def generate_quiz(subject: str, question_count: int, choice_count: int):
    print('Generating quiz questions...')
    generated_questions = generate_questions(
        subject=subject, question_count=question_count, choice_count=choice_count)
