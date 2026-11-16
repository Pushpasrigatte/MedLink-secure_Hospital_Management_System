MedLink – Hospital Management System
MedLink is a Python Flask web application developed as an academic project to support hospital management and communication between patients, doctors, laboratories, and administrators.
Features
- Role-based registration, login, and dashboards
- Patient–doctor and laboratory–doctor messaging
- Image sharing
- MySQL database integration
- Fernet-based message encryption

  Technologies Used
Programming Language: Python (likely Python 3.x).
Web Framework: Flask (micro-framework for web routing and templates).
Database: MySQL (via a MySQL connector for Flask). The schema (db.sql) defines tables for users, patients, hospitals, etc.
Libraries: Common Python libraries (such as flask_mysqldb, pyotp for OTP, email/SMS APIs, and pycryptodome or cryptography for RSA) – actual libraries should be listed in requirements.txt.
Frontend: HTML templates (Flask/Jinja2), CSS, JavaScript. (Specific CSS/JS frameworks not provided.)
Tools: Git for version control. (No deployment scripts or Docker configs were included.)

Project Structure
Add the actual folder/file structure from the project. For example:

MedLink-Hospital-Management-System/
├── app.py                 # Main Flask application
├── db.sql                 # Database schema and seed data
├── templates/             # HTML template files (login.html, dashboard.html, etc.) *
├── static/                # Static files (CSS, JS, images) *
├── README.md              # Project documentation (you are reading)
└── requirements.txt       # Python package dependencies *
