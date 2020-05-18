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
  │   │   ├── main.css                # Contain compiled styles from ths scss file
  │   │   ├── ...
  │   ├── images
  │   │   ├── ...
  │   ├── js
  │   │   ├── ...
  │   ├── scss 
  │   │   ├── main.scss
  ├── templates
  │   ├── 404.html
  │   ├── book.html
  │   ├── error.html
  │   ├── index.html
  │   ├── layout.html
  │   ├── login.html
  │   ├── register.html
  ├── .gitignore
  ├── application.py
  ├── books.csv
  ├── db.sql
  ├── import.py
  ├── README.md
  ├── requirements.txt
  ├── utils.py
