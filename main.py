import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


def generate_questions(subject: str, question_count: int, option_count: int):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    with open('quiz_sample.json', 'r') as file:
        quiz_sample = json.dumps(json.load(file))

    prompt = (f"Given the subject below, generate a series of {question_count} quiz questions on the subject."
              f"Each question should have {option_count} options, of which exactly 1 option is correct and the rest are incorrect."
              f"Format your response as a JSON list as per the following example:\n"
              f"{quiz_sample}"
              f"\nThe subject is as follows: {subject}")

    try:
        response = model.generate_content(prompt)
        response_text = response.text
        questions = json.loads(response_text)
        return questions

    except Exception as err:
        print("Error generating response from Gemini:", err)
        return


def create_quiz(subject: str, question_count: int, option_count: int):
    questions = generate_questions(
        subject=subject, question_count=question_count, option_count=option_count)
    
    print(questions)


if __name__ == '__main__':
    create_quiz(subject='computer networking',
                question_count=5, option_count=4)
