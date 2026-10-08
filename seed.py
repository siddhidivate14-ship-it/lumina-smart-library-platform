from datetime import date, timedelta
from app import app
from extensions import db
from models import User, Book, Member, Loan

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(name="Siddhi Divate", email="admin@lumina.local", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)

    books = [
        Book(title="Atomic Habits", author="James Clear", isbn="9780735211292", category="Self Growth", publisher="Avery", year=2018, quantity=8, available=6),
        Book(title="Clean Code", author="Robert C. Martin", isbn="9780132350884", category="Technology", publisher="Prentice Hall", year=2008, quantity=6, available=5),
        Book(title="Deep Work", author="Cal Newport", isbn="9781455586691", category="Productivity", publisher="Grand Central", year=2016, quantity=5, available=5),
        Book(title="Designing Data-Intensive Applications", author="Martin Kleppmann", isbn="9781449373320", category="Technology", publisher="O'Reilly", year=2017, quantity=4, available=3),
        Book(title="The Pragmatic Programmer", author="David Thomas", isbn="9780135957059", category="Technology", publisher="Addison-Wesley", year=2019, quantity=5, available=4),
        Book(title="The Psychology of Money", author="Morgan Housel", isbn="9780857197689", category="Finance", publisher="Harriman House", year=2020, quantity=7, available=7),
    ]
    db.session.add_all(books)

    members = [
        Member(member_code="LIB-2026-001", name="Aarav Sharma", email="aarav@example.com", phone="9876543210", department="Computer Science"),
        Member(member_code="LIB-2026-002", name="Ananya Patil", email="ananya@example.com", phone="9876501234", department="AI & Data Science"),
        Member(member_code="LIB-2026-003", name="Rohan Joshi", email="rohan@example.com", phone="9823456710", department="Information Technology"),
        Member(member_code="LIB-2026-004", name="Meera Kulkarni", email="meera@example.com", phone="9812345670", department="Electronics"),
    ]
    db.session.add_all(members)
    db.session.flush()

    db.session.add_all([
        Loan(book=books[0], member=members[0], due_date=date.today() + timedelta(days=8)),
        Loan(book=books[1], member=members[1], due_date=date.today() - timedelta(days=2)),
        Loan(book=books[3], member=members[2], due_date=date.today() + timedelta(days=12)),
    ])
    db.session.commit()
    print("Seed complete. Login: admin@lumina.local / admin123")
