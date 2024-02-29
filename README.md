# quiz-api
An API server for creating and fetching AI-generated quizzes

# Getting started

## Obtaining a Gemini API key
[Create an API key](https://aistudio.google.com/app/apikey) to use Google's Gemini API, which will be used to generate quizzes

## Installation and setup
1. Clone the repository and navigate to its directory
```
git clone https://github.com/Glenn-Chiang/quiz-api
cd quiz-api
```
2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Create a `.env` file and set the value of the `GEMINI_API_KEY` environment variable to your Gemini API key
```
GEMINI_API_KEY='your_api_key_here'
```
5. Initialize the database
```
flask db init
flask db migrate
flask db upgrade
```
6. Run the server
```
flask run
```

## Usage
