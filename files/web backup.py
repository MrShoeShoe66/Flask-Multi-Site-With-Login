from flask import Flask,render_template,request,redirect,url_for

import json

app = Flask(__name__)

web_online = {}
web_online['online'] = True

with open('status/web.json', 'w') as outfile:
    json.dump(web_online, outfile)

@app.route('/')
def home():
    print("Web server pinged")
    return 'e'

@app.route('/accses-denied/api')
def api():
    print("Web server pinged")
    return 'api accses denied'

@app.route('/kill')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    print("Web Server Crashed")
    web_online['online'] = False
    with open('status/web.json', 'w') as outfile:
        json.dump(web_online, outfile)
    return "Shut Web Server Down"

print("Booting Web Server")
app.run(debug=True, host="0.0.0.0", port=80)
print("Web Server Crashed")

web_online['online'] = False

with open('status/web.json', 'w') as outfile:
    json.dump(web_online, outfile)