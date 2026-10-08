from datetime import date

from flask import Blueprint, render_template
from flask_login import login_required

from extensions import db
from models import Book, Member, Loan

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    total_books = db.session.query(db.func.sum(Book.quantity)).scalar() or 0
    available_books = db.session.query(db.func.sum(Book.available)).scalar() or 0
    member_count = Member.query.count()

    active_loans = Loan.query.filter_by(status="Issued").count()

    overdue = Loan.query.filter(
        Loan.status == "Issued",
        Loan.due_date < date.today()
    ).count()

    recent_loans = (
        Loan.query
        .order_by(Loan.issue_date.desc())
        .limit(6)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_copies=total_books,
        available_copies=available_books,
        member_count=member_count,
        active_loans=active_loans,
        overdue=overdue,
        recent_loans=recent_loans,
        today=date.today(),
    )