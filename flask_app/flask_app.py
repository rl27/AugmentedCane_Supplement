'''
Set parameters:
http://raymondl.pythonanywhere.com/submit?parameters=[4.5,0.2,1.5]

Run 1 trial:
http://raymondl.pythonanywhere.com/submit?trial=1

Run trials in randomized order using specific parameters, without affecting the state of the CMA system
raymondl.pythonanywhere.com/submit?presets=[[1,1,1],[3,0.5,0.5],[7,0.2,3]]     <-- this will use the given values
raymondl.pythonanywhere.com/submit?presets=[]                                  <-- this will use the upper and lower bounds defined in TestModule.cs

Manually input a CMA sample:
http://raymondl.pythonanywhere.com/submit?sample=9.32

Load CMA state from file:
http://raymondl.pythonanywhere.com/submit?file=CMA_1854167606&count=7

{
    "commands": [
        {"trial": 10},
        {"presets": [[4.5,0.3,1.5]]},
        {"presets": [[1,0.1,1],[5,0.5,0.5]], "headings": [[40,50,70],[30,60,90]]},
        {"parameters": [4.5,0.2,1.5]}
    ]
}
'''

from flask import Flask, request
import json
import datetime
import os
import ast

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/all', methods=['POST'])
def savetojson():
    curtime = str(datetime.datetime.now())
    date = curtime.split()[0]
    time = curtime.split()[1].split(':')

    data = request.get_json()
    filename = "{0}_{1}-{2}-{3}_{4}.json".format(date, time[0], time[1], time[2][:2], data['filename'])
    with open(filename, 'w') as f:
        json.dump(data, f)

    return 'Hello'

@app.route('/submit', methods=['GET'])
def submit():
    sample = request.args.get('sample')
    file = request.args.get('file')
    count = request.args.get('count')
    parameters = request.args.get('parameters')
    trial = request.args.get('trial')
    presets = request.args.get('presets')
    headings = request.args.get('headings')
    command = {}
    if sample is not None:
        command = {'sample': sample}
    elif file is not None and count is not None:
        command = {'file': file, 'count': count}
    elif parameters is not None:
        command = {'parameters': ast.literal_eval(parameters)}
    elif trial is not None:
        command = {'trial': trial}
    elif presets is not None:
        command = {'presets': ast.literal_eval(presets)}
        if headings is not None:
            command['headings'] = ast.literal_eval(headings)

    with open('command.json', 'w') as f:
        json.dump(command, f)
    return command

@app.route('/retrieve', methods=['GET'])
def retrieve():
    command = ''
    with open('command.json', 'r+') as f:
        command = json.load(f)
        f.seek(0)
        json.dump({}, f)
        f.truncate()
    if command != {}:
        if 'file' in command and 'count' in command:
            response = {}
            file = command['file'] + '.json'
            count = command['count']
            if os.path.exists(file):
                with open(file, 'r') as f:
                    data = json.load(f)
                try:
                    count = int(count)
                except:
                    count = len(data['inputs'])
                response['inputs'] = data['inputs'][:count]
                response['outputs'] = data['outputs'][:count]
                response['seed'] = data['seed']
            return response
        return command
    return {}

@app.route('/append', methods=['POST'])
def append():
    newData = request.get_json()
    filename = "{0}.json".format(newData['filename'])
    if not os.path.exists(filename):
        with open(filename, 'w+') as f:
            data = {}
            data['inputs'] = [newData['inputs']]
            data['outputs'] = [newData['outputs']]
            data['means'] = [newData['means']]
            data['sigmas'] = [newData['sigmas']]
            data['seed'] = newData['seed']
            data['filename'] = newData['filename']
            json.dump(data, f)
    else:
        with open(filename, 'r+') as f:
            data = json.load(f)
            data['inputs'].append(newData['inputs'])
            data['outputs'].append(newData['outputs'])
            data['means'].append(newData['means'])
            data['sigmas'].append(newData['sigmas'])
            data['seed'] = newData['seed']
            data['filename'] = newData['filename']
            f.seek(0)
            json.dump(data, f)
    return 'Hello'