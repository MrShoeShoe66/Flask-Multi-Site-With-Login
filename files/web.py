from flask import Flask,render_template,request,redirect,url_for
from flask_login import login_required, current_user, login_user, logout_user, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import json

app = Flask(__name__)
app.secret_key = 'database_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login = LoginManager()
db = SQLAlchemy()

class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

db.init_app(app)
login.init_app(app)
login.login_view = 'login'

@app.before_first_request
def create_all():
    db.create_all()

@app.route('/')
def home():
    return render_template('web/home.html')

@app.route('/user/home')
@login_required
def blog():
    return render_template('web/logged in.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('blog'))
     
    return render_template('web/login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
             
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('web/register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog'))

web_online = {}
web_online['online'] = True

with open('files/status/web.json', 'w') as outfile:
    json.dump(web_online, outfile)

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