import json
import sys
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from gpiozero import LED
from time import sleep

app = Flask(__name__)
#CORS(app, origins=["http://localhost:80","http://localhost:80"])
#CORS(app, resources={r"/program": {"origins": "http://localhost:80"}})

@app.route('/')
def index():
    return 'Hello, World!'

class ProgramThread(threading.Thread):

        def __init__(self):
                super().__init__()
                self._stop_event = threading.Event()

        def stop(self):
                self._stop_event.set()

        def restart(self):
                self._stop_event.clear()

        def run(self):
                led = LED(17)
                while True:
                        if not self._stop_event.is_set():
                                led.on()
                                sleep(1)
                                led.off()
                                sleep(1)
programThread = ProgramThread()
programThread.start()


@app.route('/start', methods=['GET'])
@cross_origin(origin='*')
def startProgram():
        programThread.restart()
        return jsonify({'status':'success'})

@app.route('/stop', methods=['GET'])
@cross_origin(origin='*')
def stopProgram():
        programThread.stop()
        return jsonify({'status':'success'})

@app.route('/program', methods=['GET', 'POST'])
@cross_origin(origin='*')
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
        serve(app, host="0.0.0.0", port=5000)

