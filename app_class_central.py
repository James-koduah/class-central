from flask import abort, request, session
from flask import Flask, redirect, jsonify, render_template, make_response, g
import requests
from utils import auth_user
from mongodb_engine.users import users
from flask_cors import CORS
from blueprints.dashboard import dashboard
app = Flask(__name__)
CORS(app)
app.secret_key = '499u3u92u402u3uu44u2u01u4u4i'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

app.register_blueprint(dashboard)

@app.route('/')
def home():
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['post', 'get'], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        if not email or not password:
            return render_template('auth/login.html', error='Missing Feilds')
        user = users.login_user(email=email, password=password)
        if user == None:
            return render_template('auth/login.html', error='Sorry, Wrong Email')
        if user == False:
            return render_template('auth/login.html', error='Wrong Password', email=email)
        session['user'] = user['_id']
        return redirect('/dashboard')
    return render_template('auth/login.html')

@app.route('/logout', strict_slashes=False)
def logout():
    session.clear()
    return redirect('/')

@app.route('/signup', methods=['post', 'get'], strict_slashes=False)
def signup():
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        password2 = request.form.get('password2', None)
        if not email or not password or not password2:
            return render_template('auth/signup.html', error='Missing Feilds')
        if password != password2:
            return render_template('auth/signup.html', error='Passwords must match', email=email)
        user_id = users.signup_user(email=email, password=password)
        if not user_id:
            return render_template('auth/signup.html', error='Email already in use')
        session['user'] = user_id 
        return redirect('/dashboard')
    return render_template('auth/signup.html')





if __name__ == '__main__':
   app.run('0.0.0.0', port='5000', debug=True)
