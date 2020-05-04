import os

from flask import Flask, session, render_template, url_for, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

from utils import set_password, get_password

load_dotenv()

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL_LOCAL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL_LOCAL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return render_template('index.html', index=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))

    username = request.form.get('username')
    email = request.form.get("email")
    password = request.form.get("password")

    hashedPassword = set_password(f'{password}')

    if request.method == 'POST':
        db.execute("INSERT  INTO users (username, email, password) VALUES (:username, :email, :password)",
            {"username": username, "email": email, "password": hashedPassword})
        db.commit()
        print(f'{username, email, hashedPassword}')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title="Register", register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if request.method == 'POST':
        userData = db.execute("SELECT * FROM users WHERE username = :username", {"username": f'{username}'})
        user = []
        for item in userData:
            user.append(item)
        hashedPass = user[0][3]
        
        if user and get_password(hashedPass, password):
            session['user_id'] = user[0][0]
            session['username'] = user[0][1]

            return redirect(url_for('index'))

    return render_template('login.html', title="Login", login=True)

@app.route('/logout')
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))
