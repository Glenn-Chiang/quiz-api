from flask import Flask

app = Flask(__name__)

@app.get('/')
def index():
    return 'Hello world!'

from app import routes
from app import models