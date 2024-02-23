from uuid import uuid4
from typing import List
from question_generator import generate_questions
from models import Question, Option
from db import execute_query

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

    for generated_question in generated_questions:
        try:
            question_id = uuid4().hex
            text: str = generated_question['question']
            options: List = generated_question['options']

            questions.append(
                Question(id=question_id, text=text, quiz_id=quiz_id))
            question_options.extend([Option(
                text=option['text'], is_correct=option['correct'], question_id=question_id, quiz_id=quiz_id) for option in options])
            
        except Exception as err:
            print('Error parsing generated question:', err)
            return

    

if __name__ == '__main__':
    create_quiz(subject='programming', question_count=10, option_count=4)
