import json
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173","http://localhost:5173"])

@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/program', methods=['GET', 'POST'])
def programData():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('POST:', post_data)
        with open('program.json', 'w') as f:
            f.write(json.dumps(post_data))
        response_object['message'] = 'Program changed!';
    else:    
        with open('program.json') as f:
            programdata = json.load(f)
            #print(response, file=sys.stderr)
            response_object['programdata'] = programdata;
    return jsonify(response_object)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
