import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL_LOCAL = os.getenv("DATABASE_URL_LOCAL")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(os.getenv("DATABASE_URL_LOCAL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

  # db.execute("DROP TABLE IF EXISTS users, books, reviews")
  # print("Dropped")

  # users = '''CREATE TABLE IF NOT EXISTS users (
  #   id SERIAL PRIMARY KEY,
  #   username VARCHAR NOT NULL UNIQUE,
  #   email VARCHAR NOT NULL UNIQUE,
  #   password VARCHAR NOT NULL
  # )'''

  # books = '''CREATE TABLE IF NOT EXISTS books (
  #   id SERIAL PRIMARY KEY,
  #   title VARCHAR NOT NULL,
  #   author VARCHAR NOT NULL,
  #   years VARCHAR NOT NULL,
  #   isbn VARCHAR NOT NULL,
  #   review_count INTEGER DEFAULT 0,
  #   average_score  DECIMAL DEFAULT 0
  #   )'''

  # reviews = '''CREATE TABLE IF NOT EXISTS reviews (
  #   id SERIAL PRIMARY KEY,
  #   rating INTEGER NOT NULL DEFAULT 0,
  #   comments VARCHAR NOT NUll,
  #   author VARCHAR NOT NUll,
  #   user_id INTEGER REFERENCES users,
  #   book_id INTEGER REFERENCES books
  #   )'''

  # schema = [users, books, reviews]
  # # Create tables
  # numOfTable = 0
  # for query in schema:
  #   db.execute(query)
  #   numOfTable += 1
  #   print(f"{numOfTable} table(s) created!")
  # db.commit()

  # Insert book data from csv file
  f = open("books.csv")
  reader = csv.reader(f)
  for isbn, author, title, years in reader:
    db.execute("INSERT INTO books (isbn, author, title, years) VALUES (:isbn, :author, :title, :years)", 
      {"isbn": isbn, "author": author, "title": title, "years": years})

  db.commit()
  print("Added all the books!")

if __name__ == "__main__":
  main()