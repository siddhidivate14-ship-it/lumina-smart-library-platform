from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import or_
from extensions import db
from models import Book

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    query = Book.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Book.title.ilike(like), Book.author.ilike(like), Book.isbn.ilike(like)))
    if category:
        query = query.filter_by(category=category)
    books = query.order_by(Book.title.asc()).all()
    categories = [r[0] for r in db.session.query(Book.category).distinct().order_by(Book.category).all()]
    return render_template("books/index.html", books=books, categories=categories, q=q, category=category)

@books_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        if Book.query.filter_by(isbn=isbn).first():
            flash("A book with this ISBN already exists.", "danger")
            return render_template("books/form.html", book=None)
        quantity = max(int(request.form.get("quantity", 1)), 1)
        book = Book(
            title=request.form.get("title", "").strip(),
            author=request.form.get("author", "").strip(),
            isbn=isbn,
            category=request.form.get("category", "General").strip(),
            publisher=request.form.get("publisher", "").strip(),
            year=int(request.form.get("year")) if request.form.get("year") else None,
            quantity=quantity,
            available=quantity,
            cover_url=request.form.get("cover_url", "").strip(),
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added to the collection.", "success")
        return redirect(url_for("books.index"))
    return render_template("books/form.html", book=None)
