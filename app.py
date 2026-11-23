from flask import Flask, request, redirect, render_template_string
from database import load_books, add_book, delete_book

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>CampusLibrary</title>
<style>
body {
    font-family: Arial;
    background: #eef2ff;
    margin: 0;
}
header {
    background: #312e81;
    color: white;
    padding: 25px;
    text-align: center;
}
nav {
    background: #4338ca;
    padding: 15px;
    text-align: center;
}
nav a {
    color: white;
    margin: 15px;
    text-decoration: none;
}
.container {
    background: white;
    margin: 30px auto;
    padding: 25px;
    max-width: 850px;
    border-radius: 12px;
}
input {
    padding: 12px;
    margin: 8px;
}
button {
    padding: 10px 18px;
    background: #4338ca;
    color: white;
    border: none;
    cursor: pointer;
}
table {
    width: 100%;
    border-collapse: collapse;
}
td, th {
    padding: 12px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}
</style>
</head>
<body>
<header>
<h1>📚 CampusLibrary</h1>
<p>Library Management System</p>
</header>
<nav>
<a href="/">Dashboard</a>
<a href="/books">Books</a>
<a href="/add">Add Book</a>
</nav>
<div class="container">
{{ content|safe }}
</div>
</body>
</html>
"""

def page(content):
    return render_template_string(HTML, content=content)

@app.route("/")
def home():
    books = load_books()
    total = sum(b["quantity"] for b in books)
    available = sum(b["available"] for b in books)

    return page(f"""
    <h2>Welcome to CampusLibrary!</h2>
    <h3>Total Books: {total}</h3>
    <h3>Available Books: {available}</h3>
    <p>Manage your college library easily.</p>
    <a href="/add">Add a New Book</a>
    """)

@app.route("/books")
def books():
    all_books = load_books()
    rows = ""

    for b in all_books:
        rows += f"""
        <tr>
        <td>{b['id']}</td>
        <td>{b['title']}</td>
        <td>{b['author']}</td>
        <td>{b['quantity']}</td>
        <td>{b['available']}</td>
        <td><a href="/delete/{b['id']}">Delete</a></td>
        </tr>
        """

    return page(f"""
    <h2>Book Collection</h2>
    <table>
    <tr>
    <th>ID</th><th>Title</th><th>Author</th>
    <th>Quantity</th><th>Available</th><th>Action</th>
    </tr>
    {rows}
    </table>
    """)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        quantity = int(request.form["quantity"])

        if title.strip() and author.strip() and quantity > 0:
            add_book(title, author, quantity)

        return redirect("/books")

    return page("""
    <h2>Add New Book</h2>
    <form method="post">
    <input name="title" placeholder="Book Title" required>
    <input name="author" placeholder="Author Name" required>
    <input name="quantity" type="number" min="1"
           placeholder="Quantity" required>
    <button type="submit">Add Book</button>
    </form>
    """)

@app.route("/delete/<int:book_id>")
def delete(book_id):
    delete_book(book_id)
    return redirect("/books")

if __name__ == "__main__":
    app.run(debug=True)