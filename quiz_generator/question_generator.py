import os
import json
import jsonschema
from jsonschema.exceptions import ValidationError
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SAMPLE_OUTPUT_FILE = 'sample_output.json'
OUTPUT_SCHEMA_FILE = 'output_schema.json'


def generate_questions(subject: str, question_count: int, choice_count: int):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    with open(SAMPLE_OUTPUT_FILE, 'r') as file:
        quiz_sample = json.dumps(json.load(file))

    prompt = (f"Given the subject below, generate a series of {question_count} quiz questions on the subject."
              f"Each question should have {choice_count} options, of which only 1 option is correct and the rest are incorrect."
              f"Format your response as a JSON list as per the following example:\n"
              f"{quiz_sample}"
              f"\nThe subject is as follows: {subject}")

    try:
        response = model.generate_content(prompt)
        response_text = response.text
    except Exception as error:
        print(f'Error generating response from gemini:', error)
        return

    output_json = json.loads(response_text)
    # Check if gemini returned output in correct format
    try:
        validate_output(output_json)
        return output_json
    except ValidationError as error:
        print('Invalid output:', error)
        return


def validate_output(output):
    with open(OUTPUT_SCHEMA_FILE, 'r') as schema_file:
        schema = json.load(schema_file)
    jsonschema.validate(instance=output, schema=schema)


if __name__ == '__main__':
    questions = generate_questions(subject='computer networking',
                                   question_count=5, choice_count=4)
    print(questions)
