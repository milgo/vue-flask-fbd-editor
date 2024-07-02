import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173","http://localhost:5173"])

@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/program')
def getProgramData():
    with open('program.json') as f:
        response = json.load(f)
        return response
