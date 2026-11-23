import json
import os

FILE = "books.json"

def load_books():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_books(books):
    with open(FILE, "w") as f:
        json.dump(books, f, indent=4)

def add_book(title, author, quantity):
    books = load_books()
    book = {
        "id": len(books) + 1,
        "title": title,
        "author": author,
        "quantity": quantity,
        "available": quantity
    }
    books.append(book)
    save_books(books)

def delete_book(book_id):
    books = load_books()
    books = [b for b in books if b["id"] != book_id]
    save_books(books)