# Project 1

Web Programming with Python and JavaScript

My name is Dramane Doumbia from Mali  🇲🇱

This is a Book review website

The site let readers leaving some note on their favorite book, say something about it and see popular books that they might like to read.
They can search for a book by it's name, it author's name or by the isbn number, select the book to view all it's details and may be leave a review on the book after they have been created an account and loged in.

# Features: 
   - Search for in the home page
   - Select a Book in the results to view it's details
   - In the detail page view other person reviews, the Book ranking
   - Register an account to be able to review a book
   - Log into your account
   - Make a review after loged in

# Intallation:

## Prerequisites
Python 3

### For the dependencies look at ` requirements.txt `

## Installation:

install the dependencies from ` requirements.txt `
by runing

```
$ pip3 install -r requirements.txt
```

To run the app do the following command: 

this will run the app in production mode.

```
$ export FLASK_APP=application.py

$ flask run
```

For the debug mode you need  to run these command:

```
$ export FLASK_APP=application.py

$ export FLASK_EN=development

$ flask run
```

# Implementation details

Project structures:

    .
    ├── static
    │   ├── css
    │   │   ├── ...
    │   │   ├── main.css            # Contain compiled styles from ths scss file
    │   │   ├── ...
    │   ├── images                  # All the images in the project are here 
    │   │   ├── ...
    │   ├── js                      # Js dependencies
    │   │   ├── ...
    │   ├── scss 
    │   │   ├── main.scss           # Project styles defined here
    ├── templates
    │   ├── 404.html                # Page not found template contain meaningful message for the user and a link to home page
    │   ├── book.html               # The book details page ( book details setcion, details from goodreads section, review form, local reviews for book display list )
    │   ├── index.html              # The home page contain search form and display search results
    │   ├── layout.html             # The base layout which contain the navbar elements and the flash meassage display container
    │   ├── login.html              # The login form with two fields for username, password and submit button
    │   ├── register.html           # Register form with three fields for username, email, password and submit button
    ├── .gitignore                  # ignore files from being tracked
    ├── application.py              # The main application file with all the routes and related logics ( home route `/` with search logic, 404 route `/404` for custom 404 page, register route `/register` with registration logics, login route `/login` sign in logics, logout route `/logout` to clear user from the session, book details route `/book/id` for fetching book data, make request to goodreads api for this book data, submitting review into database and update the book info in database as well )
    ├── books.csv                   # All the book data to be inserted in the database
    ├── db.sql                      # Database schema ( tables books, users, reviews )
    ├── import.py                   # Connect to the database, create table if not existe, grab data in book.csv and insert them in the respective columns in books table
    ├── README.md                   # Project details
    ├── requirements.txt            # All the dependencies for this project to functionne
    ├── utils.py                    # Some helper functions for the password hash
