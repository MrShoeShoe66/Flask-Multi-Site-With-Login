from flask import Flask, render_template, url_for
import json

app = Flask(__name__)

@app.route('/')
def get_online():
    with open('files/status/api.json') as json_file:
        api_online_status = json.load(json_file)
    api_online = api_online_status['online']
    with open('files/status/web.json') as json_file:
        web_online_status = json.load(json_file)
    web_online = web_online_status['online']
    if api_online:
        api_ = 1
    else:
        api_ = 0
    if web_online:
        web_ = 1
    else:
        web_ = 0
    if api_ == 1 and web_ == 1:
        return render_template('/status/index.html', api='Online', web='Online', status='Online')
    elif api_ == 1 and web_ == 0:
        return render_template('/status/index.html', api='Online', web='Offline', status='Online')
    elif api_ == 0 and web_ == 0:
        return render_template('/status/index.html', api='Offline', web='Offline', status='Online')
    elif api_ == 0 and web_ == 1:
        return render_template('/status/index.html', api='Offline', web='Online', status='Online')
    else:
        return 'A System Error Occored'

app.run(debug=True, host='0.0.0.0', port=82)