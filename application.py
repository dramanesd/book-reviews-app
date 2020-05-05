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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        searchTerm = request.form.get('search')

        searchResults = db.execute("SELECT id, isbn, title, author, years FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author", 
            {"isbn": f'%{searchTerm}%', "title": f'%{searchTerm}%', "author": f'%{searchTerm}%'}).fetchall()
        results = []
        for result in searchResults:
            book = dict()
            book['id'] = result[0]
            book['isbn'] = result[1]
            book['title'] = result[2]
            book['author'] = result[3]
            book['years'] = result[4]
            results.append(book)

        # print(results)
        return render_template('index.html', results=results, index=True)

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
        # print(f'{username, email, hashedPassword}')
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
        user = dict()
        for item in userData:
            u = dict()
            u['user_id'] = item[0]
            u['username'] = item[1]
            u['password'] = item[3]
            user = u
        # print(user["password"])
        hashedPass = user["password"]
        
        if user and get_password(hashedPass, password):
            session['user_id'] = user["user_id"]
            session['username'] = user["username"]

            return redirect(url_for('index'))

    return render_template('login.html', title="Login", login=True)

@app.route('/logout')
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book(id):
    bookResults = db.execute("SELECT * FROM books WHERE id = :id", {"id": id}).fetchall()
   
    book = []
    for item in bookResults:
        i = dict()
        i['book_id'] = item[0]
        i['title'] = item[1]
        i['author'] = item[2]
        i['years'] = item[3]
        i['isbn'] = item[4]
        i['review_count'] = item[5]
        i['average_score'] = item[6]
        book.append(i)
    print(book)

    reviewResults = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": id}).fetchall()
    reviews = []
    for item in reviewResults:
        i = dict()
        i['rating'] = item[1]
        i['comments'] = item[2]
        i['author'] = item[3]
        reviews.append(i)
    # print(session)

    if request.method == 'POST' and session['user_id'] != False:
        ratValue = request.form.get('rat')
        comment = request.form.get('comment')
        book_id = id
        user_id = session['user_id']
        username = session['username']
        
        bookIdCheck = db.execute("SELECT book_id FROM reviews WHERE user_id = :user_id", {"user_id": user_id}).fetchone()

        if bookIdCheck == None or bookIdCheck[0] != book_id:
            db.execute("INSERT INTO reviews (rating, comments, author, user_id, book_id) VALUES (:rating, :comments, :author, :user_id, :book_id)", 
                {"rating": ratValue, "comments": comment, "author": username, "user_id": user_id, "book_id": book_id})
            db.commit()

            review_count = bookResults[0][5]
            avg = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).fetchone()
            # print(f'Avg = {avg[0]}')
            db.execute("UPDATE books SET review_count = :plusOne, average_score = :avg WHERE id = :book_id", 
                {"plusOne": review_count+1, "avg": avg[0], "book_id": book_id})
            db.commit()
        else:
            print("You already commented on this book!")
            return redirect(url_for('book', id=book_id))

    return render_template('book.html', id=id, bookDetails=book, reviews=reviews, book=True)