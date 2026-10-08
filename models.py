from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="librarian")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False, index=True)
    author = db.Column(db.String(160), nullable=False)
    isbn = db.Column(db.String(30), unique=True, nullable=False, index=True)
    category = db.Column(db.String(80), nullable=False, default="General")
    publisher = db.Column(db.String(160))
    year = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    available = db.Column(db.Integer, nullable=False, default=1)
    cover_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(30))
    department = db.Column(db.String(120))
    joined_at = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(30), nullable=False, default="Active")

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    issue_date = db.Column(db.Date, default=date.today, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(30), nullable=False, default="Issued")
    book = db.relationship("Book", backref=db.backref("loans", lazy=True))
    member = db.relationship("Member", backref=db.backref("loans", lazy=True))

    @property
    def fine_amount(self):
        end_date = self.return_date or date.today()
        days_late = max((end_date - self.due_date).days, 0)
        return days_late * 10
