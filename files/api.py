from flask import Flask, redirect, request
import json

app = Flask(__name__)

api_online = {}
api_online['online'] = True

with open('files/status/api.json', 'w') as outfile:
    json.dump(api_online, outfile)

@app.route('/')
def home():
    return redirect('http://10.0.1.124/accses-denied/api')

@app.route('/kill')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    print("Web Server Crashed")
    api_online['online'] = False
    with open('status/api.json', 'w') as outfile:
        json.dump(api_online, outfile)
    return "Shut API Server Down"

@app.errorhandler(404)
def err_404():
    return redirect('http://10.0.1.124/accses-denied/api')

print("Booting API Server")
app.run(debug=True, host="0.0.0.0", port=81)
print("API Server Chrashed")

api_online['online'] = False

with open('status/api.json', 'w') as outfile:
    json.dump(api_online, outfile)