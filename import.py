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
  f = open("books.csv")
  reader = csv.reader(f)
  for isbn, author, title, years in reader:
    db.execute("INSERT INTO books (isbn, author, title, years) VALUES (:isbn, :author, :title, :years)", 
      {"isbn": isbn, "author": author, "title": title, "years": years})

  db.commit()
  print("Added all the books!")

if __name__ == "__main__":
  main()