# Certify - Certification Management System

A scalable Certification Management System built using FastAPI that manages candidate registrations, certification workflows, examination scheduling, credential verification, role-based access control, and continuous learning requirements.

---

## Features

- JWT Authentication & Authorization
- Role Based Access Control (RBAC)
- User Registration & Login
- Certification Management
- Examination Slot Management
- Continuous Learning Tracking
- MOC (Maintenance of Certification)
- AWS S3 Certificate Storage
- Email Notifications
- PostgreSQL Integration
- Alembic Database Migrations
- Secure Password Hashing
- Super Admin Seeding

---

# Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.11 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migration Tool | Alembic |
| Authentication | JWT |
| Password Hashing | Argon2 |
| Storage | AWS S3 |
| Email Service | FastAPI-Mail |
| Dependency Management | Poetry |

---

# Project Structure

```bash
.
├── alembic/
│   ├── versions/
│   └── env.py
│
├── src/
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── exceptions/
│   ├── middleware/
│   ├── model/
│   ├── repository/
│   ├── router/
│   ├── schema/
│   ├── service/
│   └── utils/
│
├── main.py
├── pyproject.toml
└── alembic.ini
```

---

# Architecture

```text
Client
   │
   ▼
FastAPI Routers
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
PostgreSQL Database
```

---

# Authentication Flow

```text
Register User
      │
      ▼
Hash Password
      │
      ▼
Store User
      │
      ▼
Generate JWT
      │
      ▼
Protected Endpoints
```

---

# Database Models

### User

- User Information
- Degree Details
- Certificate Upload
- Passing Year

### User Role

- SUPERADMIN
- ADMIN
- CANDIDATE
- DIPLOMATE
- USER

### Certification

- Certification Tracking
- Verification

### Examination Slot

- Slot Creation
- Slot Allocation

### Continuous Learning

- Learning Credits
- Tracking

### MOC

- Maintenance of Certification
- Status Tracking

---

# API Endpoints

## Authentication

| Method | Endpoint |
|----------|------------|
| POST | /auth/register |
| POST | /auth/login |
| POST | /auth/refresh_token |

---

## User Management

| Method | Endpoint |
|----------|------------|
| POST | /user/create_admin |
| GET | /user/get_user_by_email_id |
| GET | /user/get_admin |
| GET | /user/get_candidate |
| GET | /user/get_diplomate |
| GET | /user/get_user |
| GET | /user/get_all_user |

---

## Examination

| Module |
|----------|
| Slot Creation |
| Slot Allocation |
| Examination Management |

---

## Certification

| Module |
|----------|
| Certification Creation |
| Credential Verification |
| Lifecycle Management |

---

# Environment Variables

Create a `.env` file:

```env
DATABASE_URL=

SECRET_KEY=
ALGORITHM=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_BUCKET_NAME=

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_SERVER=
MAIL_PORT=

SUPERADMIN_EMAIL=
SUPERADMIN_PASSWORD=
SUPERADMIN_FIRST_NAME=
SUPERADMIN_LAST_NAME=
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/certify-backend.git

cd certify-backend
```

---

## Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
poetry install
```

---

## Configure Environment Variables

```bash
cp .env.example .env
```

Update values accordingly.

---

## Run Migrations

```bash
alembic upgrade head
```

---

## Start Application

```bash
uvicorn main:app --reload
```

---

# API Documentation

Swagger UI

```text
http://localhost:8000/docs
```

ReDoc

```text
http://localhost:8000/redoc
```

---

# Security Features

- JWT Authentication
- Password Hashing using Argon2
- Role Based Access Control
- Token Refresh Mechanism
- Protected Endpoints
- Input Validation via Pydantic

---

# Future Improvements

- Docker Support
- Kubernetes Deployment
- CI/CD Pipeline
- Redis Caching
- Audit Logging
- Event Driven Architecture
- Microservice Migration

---

# Author

**Amogh Shukla**

AI & Data Science Engineer

LinkedIn:
https://linkedin.com/in/amogh-shukla

GitHub:
https://github.com/amogh-shukla
