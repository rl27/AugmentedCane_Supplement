
# http://raymondl.pythonanywhere.com/submit?sample=9.32
# http://raymondl.pythonanywhere.com/submit?file=CMA_1854167606&count=7
# http://raymondl.pythonanywhere.com/submit?params=4.5,0.2,1.5
# http://raymondl.pythonanywhere.com/submit?trial=1
# http://raymondl.pythonanywhere.com/submit?presets=1,1,1,3,0.5,0.5,7,0.2,3     <-- this will use the given values
# http://raymondl.pythonanywhere.com/submit?presets=0                           <-- this will use the upper and lower bounds defined in TestModule.cs

# http://raymondl.pythonanywhere.com/retrieve

from flask import Flask, request
import json
import datetime
import os

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
    params = request.args.get('params')
    trial = request.args.get('trial')
    presets = request.args.get('presets')
    command = {}
    if sample is not None:
        command = {'sample': sample}
    elif file is not None and count is not None:
        command = {'file': file, 'count': count}
    elif params is not None:
        command = {'params': params.split(',')}
    elif trial is not None:
        command = {'trial': trial}
    elif presets is not None:
        command = {'presets': presets.split(',')}

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
        response = {}
        if 'sample' in command:
            response['sample'] = command['sample']
        elif 'file' in command and 'count' in command:
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
        elif 'params' in command:
            response['prms'] = command['params']
        elif 'trial' in command:
            response['trial'] = command['trial']
        elif 'presets' in command:
            response['presets'] = command['presets']
        return response
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