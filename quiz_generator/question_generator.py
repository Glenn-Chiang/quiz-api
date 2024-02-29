import os
import json
import jsonschema
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

dirname = os.path.dirname(__file__)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
RESPONSE_SAMPLE = os.path.join(dirname, 'response_sample.json')
RESPONSE_SCHEMA = os.path.join(dirname, 'response_schema.json')


def generate_questions(subject: str, question_count: int, choice_count: int):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    with open(RESPONSE_SAMPLE, 'r') as file:
        quiz_sample = json.load(file)
        quiz_sample_string = json.dumps(quiz_sample)

    prompt = (f"Given the subject below, generate a series of {question_count} quiz questions on the subject."
              f"Each question should have {choice_count} options, of which only 1 option is correct and the rest are incorrect."
              f"Format your response as a JSON list as per the following example:\n"
              f"{quiz_sample_string}"
              f"\nThe subject is as follows: {subject}")

    try:
        response = model.generate_content(prompt)
        response_text = response.text
    except Exception as error:
        print(f'Error generating response from gemini:', error)
        raise error

    # Check if gemini returned output in correct format
    try:
        output_json = json.loads(response_text)
        validate_output(output_json)
        return output_json
    except (json.JSONDecodeError or jsonschema.ValidationError) as error:
        print('Invalid output:', error)
        raise error


def validate_output(output):
    with open(RESPONSE_SCHEMA, 'r') as schema_file:
        schema = json.load(schema_file)
    jsonschema.validate(instance=output, schema=schema)


if __name__ == '__main__':
    questions = generate_questions(subject='programming',
                                   question_count=5, choice_count=4)
    print(questions)
