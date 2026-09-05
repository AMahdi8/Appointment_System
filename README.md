# Appointment System

A comprehensive appointment scheduling system for clinics and doctors, built with Django and Django REST Framework. This system provides role-based access control, appointment scheduling, and medical record management.

---

## Features

- **Role-based Access Control:** Separate roles for Admin, Doctor, and Patient.
- **Appointment Scheduling:** Flexible system for booking and managing appointments.
- **Medical Records:** Secure storage and retrieval of patient medical histories.
- **API Support:** RESTful API endpoints using Django REST Framework.
- **Task Scheduling:** Asynchronous tasks with Celery and Redis.
- **JWT Authentication:** Secure token-based authentication.
- **Automated Notifications:** SMS/email notifications for upcoming appointments.

---

## Installation

1. Clone the repository:
   git clone https://github.com/AMahdi8/appointment-system.git
   cd appointment-system

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows

3. Install the dependencies:
   pip install -r requirements.txt

4. Set up the database:
   python manage.py makemigrations
   python manage.py migrate

5. Create a `.env` file and configure the following variables:
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=localhost
   DB_PORT=5432
   CELERY_BROKER_URL=redis://localhost:6379/0

6. Run the development server:
   python manage.py runserver

---

## Usage

- **Admin Panel:** /admin/
- **API Documentation:** /api/docs/ (if configured)
- **Endpoints:**
  - /api/auth/: User authentication (login/logout/registration)
  - /api/appointments/: Appointment scheduling and management
  - /api/medical-records/: CRUD operations for medical records

---

## Environment-Based Settings

The project uses environment-specific settings divided into:
- common.py: Shared settings across environments.
- dev.py: Development-specific settings.
- prod.py: Production-specific settings.

Set the environment using:
   export DJANGO_SETTINGS_MODULE=appointment_system.settings.dev  # For development
   export DJANGO_SETTINGS_MODULE=appointment_system.settings.prod  # For production

---

## Dependencies

- Python 3.9+
- Django 5.0+
- Django REST Framework
- Celery
- Redis
- PostgreSQL

---

## Running Tests

To run the tests, use:
   pytest

---

## Deployment

1. Configure the production settings in prod.py.
2. Collect static files:
   python manage.py collectstatic
3. Use a production server like **Gunicorn** with a reverse proxy (e.g., Nginx).
4. Configure Celery and Redis for task scheduling.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
