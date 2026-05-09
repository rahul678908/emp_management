# Employee Management System

A full-featured Employee Management System built with Django + REST Framework.

## Features

### Authentication & Profile
- User Registration & Login
- JWT-based API authentication (access + refresh tokens)
- Profile management with photo upload
- Change password

### Employee Management
- **Dynamic Form Builder** — build custom forms with drag-and-drop field ordering
- **Field Types**: text, number, email, password, date, textarea, select, checkbox, tel, url
- **Employee CRUD** — create/edit employees using dynamic form templates
- **Employee Listing** — search & filter by dynamic field labels, delete records
- All form submissions via Axios (no Django form actions)

### REST API
- JWT auth endpoints (register, login, refresh, logout)
- Employee CRUD API
- Dynamic form CRUD API

## Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd emp_mgmt

# 2. Create virtualenv
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register new user |
| POST | /api/auth/login/ | Login & get JWT tokens |
| POST | /api/auth/logout/ | Logout (blacklist token) |
| POST | /api/auth/token/refresh/ | Refresh access token |
| GET/PUT | /api/auth/profile/ | View/update profile |
| POST | /api/auth/change-password/ | Change password |

### Employees
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/employees/ | List all employees |
| POST | /api/employees/ | Create employee |
| GET | /api/employees/{id}/ | Get employee detail |
| PUT | /api/employees/{id}/ | Update employee |
| DELETE | /api/employees/{id}/ | Delete employee |

### Dynamic Forms
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/forms/ | List all forms |
| POST | /api/forms/ | Create form |
| GET | /api/forms/{id}/ | Get form detail |
| PUT | /api/forms/{id}/ | Update form |
| DELETE | /api/forms/{id}/ | Delete form |

## Tech Stack
- **Backend**: Python 3.10+, Django 4.2, Django REST Framework
- **Auth**: JWT via `djangorestframework-simplejwt`
- **Frontend**: Bootstrap 5, Axios, Vanilla JS (drag-and-drop HTML5 API)
- **Database**: SQLite (dev) — swap to PostgreSQL for production
