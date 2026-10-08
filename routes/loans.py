from datetime import date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models import Book, Member, Loan

loans_bp = Blueprint("loans", __name__, url_prefix="/loans")

@loans_bp.route("/")
@login_required
def index():
    loans = Loan.query.order_by(Loan.id.desc()).all()
    books = Book.query.filter(Book.available > 0).order_by(Book.title).all()
    members = Member.query.filter_by(status="Active").order_by(Member.name).all()
    return render_template("loans/index.html", loans=loans, books=books, members=members, today=date.today())

@loans_bp.route("/issue", methods=["POST"])
@login_required
def issue():
    book = db.session.get(Book, int(request.form["book_id"]))
    member = db.session.get(Member, int(request.form["member_id"]))
    days = max(int(request.form.get("days", 14)), 1)
    if not book or book.available < 1 or not member:
        flash("Book is unavailable or member is invalid.", "danger")
        return redirect(url_for("loans.index"))
    loan = Loan(book=book, member=member, due_date=date.today() + timedelta(days=days))
    book.available -= 1
    db.session.add(loan)
    db.session.commit()
    flash(f'"{book.title}" issued to {member.name}.', "success")
    return redirect(url_for("loans.index"))

@loans_bp.route("/<int:loan_id>/return", methods=["POST"])
@login_required
def return_book(loan_id):
    loan = db.session.get(Loan, loan_id)
    if not loan or loan.status != "Issued":
        flash("This loan is already closed.", "warning")
        return redirect(url_for("loans.index"))
    loan.status = "Returned"
    loan.return_date = date.today()
    loan.book.available = min(loan.book.available + 1, loan.book.quantity)
    fine = loan.fine_amount
    db.session.commit()
    if fine:
        flash(f"Book returned. Late fine calculated: ₹{fine}.", "warning")
    else:
        flash("Book returned successfully.", "success")
    return redirect(url_for("loans.index"))
