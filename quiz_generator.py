from question_generator import generate_questions


def create_quiz(subject: str, question_count: int, option_count: int):
    try:
        questions = generate_questions(
            subject=subject, question_count=question_count, option_count=option_count)
    except Exception as err:
        print('Error generating quiz questions:', err, sep='\n')
        return
    
    print(questions)


if __name__ == '__main__':
    create_quiz(subject='', question_count=10, option_count=4)