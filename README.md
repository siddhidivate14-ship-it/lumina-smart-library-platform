# Lumina Library — Enterprise Smart Library Management Platform

A resume-ready DevOps project built with Flask, PostgreSQL, Pytest, Git/GitHub, Jenkins, Docker and Kubernetes/Minikube.

## Phase A currently included
- Responsive premium dashboard UI
- Authentication with hashed passwords
- Book catalogue and search/filter
- Member directory and registration
- Book issue/return workflow
- Automatic overdue fine calculation
- PostgreSQL-ready SQLAlchemy models
- Seed data for a realistic demo
- Pytest smoke test

## Run locally

### 1. Create environment
Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure environment
Copy `.env.example` to `.env` and set your PostgreSQL connection string.

Example:
```env
SECRET_KEY=your-long-secret
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/smart_library
```

Create the PostgreSQL database:
```sql
CREATE DATABASE smart_library;
```

### 3. Seed demo data
```powershell
python seed.py
```

### 4. Start application
```powershell
python app.py
```

Open:
http://127.0.0.1:5000

Demo:
- Email: admin@lumina.local
- Password: admin123

## DevOps roadmap
1. Complete application modules
2. Add comprehensive Pytest suite
3. Git feature branches + GitHub
4. Jenkins CI pipeline
5. Docker image
6. Kubernetes Deployment + Service
7. Minikube deployment
8. Monitoring and production hardening
