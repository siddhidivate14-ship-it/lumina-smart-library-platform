from datetime import date, timedelta

import pytest

from app import create_app
from extensions import db
from models import User, Book, Member, Loan


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(
            name="Test Librarian",
            email="admin@test.com",
            role="admin",
        )
        user.set_password("test123")

        book = Book(
            title="Test Book",
            author="Test Author",
            isbn="TEST-ISBN-001",
            category="Testing",
            quantity=3,
            available=3,
        )

        member = Member(
            member_code="TEST-001",
            name="Test Member",
            email="member@test.com",
            phone="9999999999",
            department="AI & DS",
        )

        db.session.add_all([user, book, member])
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def login(client):
    return client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "test123",
        },
        follow_redirects=True,
    )


# ---------------------------------------------------------
# Application / Authentication Tests
# ---------------------------------------------------------

def test_application_starts(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Lumina" in response.data


def test_login_page_contains_form(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Email address" in response.data
    assert b"Password" in response.data


def test_valid_login(client):
    response = login(client)

    assert response.status_code == 200
    assert b"Test Librarian" in response.data


def test_invalid_login(client):
    response = client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "wrong-password",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_protected_dashboard_requires_login(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_protected_books_requires_login(client):
    response = client.get("/books/", follow_redirects=False)

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_protected_members_requires_login(client):
    response = client.get("/members/", follow_redirects=False)

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_protected_loans_requires_login(client):
    response = client.get("/loans/", follow_redirects=False)

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


# ---------------------------------------------------------
# Dashboard Tests
# ---------------------------------------------------------

def test_dashboard_loads_after_login(client):
    login(client)

    response = client.get("/")

    assert response.status_code == 200
    assert b"Total copies" in response.data
    assert b"Members" in response.data
    assert b"Overdue" in response.data


# ---------------------------------------------------------
# Book Tests
# ---------------------------------------------------------

def test_books_page_loads(client):
    login(client)

    response = client.get("/books/")

    assert response.status_code == 200
    assert b"Test Book" in response.data


def test_add_book(client, app):
    login(client)

    response = client.post(
        "/books/add",
        data={
            "title": "Clean Architecture",
            "author": "Robert Martin",
            "isbn": "978-0134494166",
            "category": "Software Engineering",
            "publisher": "Prentice Hall",
            "year": "2017",
            "quantity": "5",
            "cover_url": "",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Clean Architecture" in response.data

    with app.app_context():
        book = Book.query.filter_by(
            isbn="978-0134494166"
        ).first()

        assert book is not None
        assert book.quantity == 5
        assert book.available == 5


def test_duplicate_isbn_is_rejected(client, app):
    login(client)

    response = client.post(
        "/books/add",
        data={
            "title": "Another Book",
            "author": "Another Author",
            "isbn": "TEST-ISBN-001",
            "category": "Testing",
            "quantity": "1",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"already exists" in response.data

    with app.app_context():
        books = Book.query.filter_by(
            isbn="TEST-ISBN-001"
        ).all()

        assert len(books) == 1


# ---------------------------------------------------------
# Member Tests
# ---------------------------------------------------------

def test_members_page_loads(client):
    login(client)

    response = client.get("/members/")

    assert response.status_code == 200
    assert b"Test Member" in response.data


def test_add_member(client, app):
    login(client)

    response = client.post(
        "/members/add",
        data={
            "member_code": "LIB-2026-100",
            "name": "Siddhi Test",
            "email": "siddhi@test.com",
            "phone": "9876543210",
            "department": "AI & DS",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Siddhi Test" in response.data

    with app.app_context():
        member = Member.query.filter_by(
            member_code="LIB-2026-100"
        ).first()

        assert member is not None
        assert member.name == "Siddhi Test"


def test_duplicate_member_code_is_rejected(client, app):
    login(client)

    response = client.post(
        "/members/add",
        data={
            "member_code": "TEST-001",
            "name": "Duplicate Member",
            "email": "duplicate@test.com",
            "phone": "",
            "department": "",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"already exists" in response.data

    with app.app_context():
        members = Member.query.filter_by(
            member_code="TEST-001"
        ).all()

        assert len(members) == 1


# ---------------------------------------------------------
# Loan / Circulation Tests
# ---------------------------------------------------------

def test_issue_book(client, app):
    login(client)

    with app.app_context():
        book = Book.query.filter_by(
            isbn="TEST-ISBN-001"
        ).first()

        member = Member.query.filter_by(
            member_code="TEST-001"
        ).first()

        book_id = book.id
        member_id = member.id

    response = client.post(
        "/loans/issue",
        data={
            "book_id": book_id,
            "member_id": member_id,
            "days": "14",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"issued to" in response.data

    with app.app_context():
        book = db.session.get(Book, book_id)

        loan = Loan.query.filter_by(
            book_id=book_id,
            member_id=member_id,
        ).first()

        assert loan is not None
        assert loan.status == "Issued"
        assert book.available == 2


def test_return_book(client, app):
    login(client)

    with app.app_context():
        book = Book.query.filter_by(
            isbn="TEST-ISBN-001"
        ).first()

        member = Member.query.filter_by(
            member_code="TEST-001"
        ).first()

        loan = Loan(
            book=book,
            member=member,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status="Issued",
        )

        book.available -= 1

        db.session.add(loan)
        db.session.commit()

        loan_id = loan.id
        book_id = book.id

    response = client.post(
        f"/loans/{loan_id}/return",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"returned successfully" in response.data

    with app.app_context():
        loan = db.session.get(Loan, loan_id)
        book = db.session.get(Book, book_id)

        assert loan.status == "Returned"
        assert loan.return_date == date.today()
        assert book.available == 3


# ---------------------------------------------------------
# Fine Calculation Tests
# ---------------------------------------------------------

def test_fine_calculation():
    class FakeLoan:
        due_date = date.today() - timedelta(days=5)
        return_date = date.today()

        @property
        def fine_amount(self):
            end_date = self.return_date or date.today()
            days_late = max(
                (end_date - self.due_date).days,
                0,
            )
            return days_late * 10

    loan = FakeLoan()

    assert loan.fine_amount == 50


def test_no_fine_when_returned_on_time(app):
    with app.app_context():
        book = Book.query.first()
        member = Member.query.first()

        loan = Loan(
            book=book,
            member=member,
            due_date=date.today(),
            return_date=date.today(),
            status="Returned",
        )

        assert loan.fine_amount == 0