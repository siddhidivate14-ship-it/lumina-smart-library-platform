# 📚 Lumina Smart Library Management Platform

**A modern, web-based library management system built with Flask and deployed on AWS EC2 using Docker.**

Lumina Smart Library brings book collection management, member administration, and book circulation into one clean, centralized workspace. It is designed to simplify everyday library operations while providing hands-on experience with web development, containerization, and cloud deployment.

## 🌐 Live Application

**Live Demo:** [Lumina Smart Library](http://3.110.41.43)

> **Deployment note:** The application is currently hosted on an AWS EC2 instance and served over HTTP. Availability depends on the instance running and its network configuration. HTTPS has not yet been configured.

## ✨ Features

- **Dashboard:** Centralized overview of library operations.
- **Book Collection:** Manage the library's book inventory and collection records.
- **Member Management:** Maintain library member information.
- **Book Circulation:** Issue books, track due dates, view loan history, and process returns.
- **Authentication:** Login-protected application pages.
- **Persistent Database:** SQLite database storage with a Docker volume in the current deployment.
- **Containerized Application:** Docker-based packaging for consistent deployment.
- **Cloud Hosting:** Application hosted on an Ubuntu EC2 instance in AWS.
- **Production-oriented Serving:** Gunicorn used to serve the Flask application.

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Backend | Python, Flask |
| Database ORM | Flask-SQLAlchemy |
| Database | SQLite by default; PostgreSQL driver included |
| Authentication | Flask-Login |
| Application Server | Gunicorn |
| Containerization | Docker |
| Cloud Platform | AWS EC2 |
| Server Operating System | Ubuntu Linux |
| Version Control | Git and GitHub |
| Testing | pytest |

## 🏗️ Architecture

```text
             User's Web Browser
                     |
                  HTTP :80
                     |
              AWS EC2 Instance
                Ubuntu Linux
                     |
                  Docker
                     |
            Gunicorn :5000
                     |
                Flask App
          ┌──────────┼──────────┐
          |          |          |
       Books      Members    Circulation
          |          |          |
          └──────────┼──────────┘
                     |
             Flask-SQLAlchemy
                     |
              SQLite Database
             Docker Volume
```

## 📂 Project Structure

```text
lumina-smart-library-platform/
├── app.py
├── extensions.py
├── models.py
├── seed.py
├── requirements.txt
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── books.py
│   ├── members.py
│   └── loans.py
├── templates/
├── static/
├── tests/
├── Dockerfile
├── .dockerignore
└── README.md
```

*The exact file structure may vary slightly depending on the latest repository version.*

## 🚀 Run Locally

### Prerequisites

- Python 3.12 or a compatible Python version
- Git
- Docker Desktop (optional if running directly with Python)

### Option 1: Run with Python

**1. Clone the repository**

```bash
git clone https://github.com/siddhidivate14-ship-it/lumina-smart-library-platform.git
cd lumina-smart-library-platform
```

**2. Create a virtual environment**

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-with-a-secure-random-secret
FLASK_DEBUG=1
PORT=5000
```

Generate a secure secret locally instead of using the example text. Do not commit `.env` to GitHub.

**5. Start the application**

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

### Option 2: Run with Docker

After installing Docker, build the image from the repository root:

```bash
docker build -t lumina-smart-library:1.0 .
```

Create a persistent Docker volume:

```bash
docker volume create lumina_data
```

Run the application:

```bash
docker run -d \
  --name lumina-library \
  --restart unless-stopped \
  -p 5000:5000 \
  -e SECRET_KEY="replace-with-your-secure-secret" \
  -e FLASK_DEBUG=0 \
  -v lumina_data:/app/instance \
  lumina-smart-library:1.0 \
  gunicorn --bind 0.0.0.0:5000 app:app
```

Open `http://localhost:5000`.

> Ensure that the Dockerfile, `.dockerignore`, and application dependencies are present before building. Keep secrets out of source control.

## ☁️ AWS EC2 Deployment

The current cloud deployment uses the following workflow:

1. Launch an Ubuntu EC2 instance.
2. Configure SSH access and HTTP access through the EC2 security group.
3. Install Git and Docker Engine.
4. Clone the GitHub repository.
5. Build the Docker image.
6. Create a Docker volume for persistent SQLite storage.
7. Run the container with Gunicorn and restart policy `unless-stopped`.
8. Map EC2 port `80` to the application's container port `5000`.
9. Access the application through the EC2 public IPv4 address.

The deployed container uses the image `lumina-smart-library:1.0` and the container name `lumina-library`.

### Useful Docker Commands

Check container status:

```bash
sudo docker ps
```

View application logs:

```bash
sudo docker logs --tail 100 lumina-library
```

Stop the application:

```bash
sudo docker stop lumina-library
```

Start it again:

```bash
sudo docker start lumina-library
```

Restart the container:

```bash
sudo docker restart lumina-library
```

The Docker volume `lumina_data` stores the database separately from the container. Do not remove this volume if you need to preserve library records.

## 🧪 Testing

The project has previously passed a local test suite containing 19 tests.

Run the tests from the project root:

```bash
python -m pytest -q
```

Run this command in your own environment to verify the current repository version.

## 🔐 Security Considerations

- Generate a unique, strong Flask `SECRET_KEY`.
- Never commit passwords, AWS credentials, private SSH keys, or `.env` files.
- Change demo credentials before sharing the application widely.
- Use HTTPS with a domain name and TLS certificate for secure public access.
- Restrict SSH port 22 to trusted IP addresses.
- Back up the database volume regularly.
- Use PostgreSQL or another appropriately managed database when production-scale concurrency and reliability are required.
- Avoid running the destructive seed script against a database containing important records.

## 🔮 Future Enhancements

- HTTPS configuration with a domain name and reverse proxy.
- Managed PostgreSQL deployment.
- Automated CI/CD pipeline for cloud releases.
- Improved monitoring, logging, and health checks.
- Automated database backups and recovery.
- Role-based permissions and stronger account management.
- Advanced inventory analytics and reporting.
- Infrastructure as Code using Terraform.

## 🎯 Learning Outcomes

This project provides practical experience with:

- Python web application development using Flask.
- Database modeling and ORM integration.
- Authentication and modular application design.
- Docker image creation and container lifecycle management.
- Gunicorn application serving.
- AWS EC2 provisioning and network access configuration.
- Linux server administration and deployment troubleshooting.
- Git-based version control and testing.

## 👩‍💻 Author

**Siddhi Divate**

Artificial Intelligence and Data Science Student

GitHub: [@siddhidivate14-ship-it](https://github.com/siddhidivate14-ship-it)

