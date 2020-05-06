import os
import requests

from flask import Flask, session, render_template, url_for, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

from utils import set_password, get_password

load_dotenv()

GOODREADS_KEY = os.getenv("GOODREADS_KEY")

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
        # Perform the search query
        searchTerm = request.form.get('search')
        searchResults = db.execute("SELECT id, isbn, title, author, years FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author", 
            {"isbn": f'%{searchTerm}%', "title": f'%{searchTerm}%', "author": f'%{searchTerm}%'}).fetchall()

        return render_template('index.html', results=searchResults, index=True)

    return render_template('index.html', index=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if user have an account and is connected
    if session.get('username'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get("email")
        password = request.form.get("password")
        # Hash the password
        hashedPassword = set_password(f'{password}')

        db.execute("INSERT  INTO users (username, email, password) VALUES (:username, :email, :password)",
            {"username": username, "email": email, "password": hashedPassword})
        db.commit()

        return redirect(url_for('login'))
    else:
        return render_template('register.html', title="Register", register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check to see if user is connected and redirect to index
    if session.get('username'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the given password and the hashed one match then let it log in
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": f'{username}'}).fetchone()
        hashedPass = user.password
        if user and get_password(hashedPass, password):
            session['user_id'] = user.id
            session['username'] = user.username

            return redirect(url_for('index'))

    return render_template('login.html', title="Login", login=True)

@app.route('/logout')
def logout():
    # Clearing session to logout
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book(id):
    # Get book data from the database for display
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": id}).fetchall()

    # Get reviews data from the database for display
    reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": id}).fetchall()

    # Make request to goodreads api to get data
    isbn = book[0][4]
    res = requests.get(f"https://www.goodreads.com/book/review_counts.json?key={GOODREADS_KEY}&isbns={isbn}")
    if res.status_code == 200:
        data = res.json()
        # Get specific data needed to send in template
        average_rating = data['books'][0]['average_rating']
        work_ratings_count = data['books'][0]['work_ratings_count']
        goodreadsData = {"average_rating": average_rating, "work_ratings_count": work_ratings_count}
        
    if request.method == 'POST' and session['user_id'] != False:
        # Get form data
        ratValue = request.form.get('rat')
        comment = request.form.get('comment')
        book_id = id
        user_id = session['user_id']
        username = session['username']
        
        # Check if user has reviewed this book before perform any operation
        bookIdCheck = db.execute("SELECT book_id FROM reviews WHERE user_id = :user_id", {"user_id": user_id}).fetchone()
        if bookIdCheck == None or bookIdCheck[0] != book_id:
            # Insert review in the database
            db.execute("INSERT INTO reviews (rating, comments, author, user_id, book_id) VALUES (:rating, :comments, :author, :user_id, :book_id)", 
                {"rating": ratValue, "comments": comment, "author": username, "user_id": user_id, "book_id": book_id})
            db.commit()
            # Updating the specific book review_count and average_score
            review_count = book[0][5]
            avg = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).fetchone()
            db.execute("UPDATE books SET review_count = :plusOne, average_score = :avg WHERE id = :book_id", 
                {"plusOne": review_count+1, "avg": avg[0], "book_id": book_id})
            db.commit()
        else:
            # Return back to book page if user already reviewed the book
            print("You already commented on this book!")
            return redirect(url_for('book', id=book_id))

    return render_template('book.html', id=id, bookDetails=book, goodreadsData=goodreadsData, reviews=reviews, book=True)

@app.route('/api/<string:isbn>')
def isbn_api(isbn):
    # Get book base on isbn
    isbn = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    # Seriliaze data to json format
    return jsonify({
        "title": isbn.title,
        "author": isbn.author,
        "year": isbn.years,
        "isbn": isbn.isbn,
        "review_count": isbn.review_count,
        "average_score": isbn.average_score
    })