# MADR API - Modern Archive for Digital Romance

A production-ready REST API for managing romance books and novelists, built with FastAPI, PostgreSQL, async SQLAlchemy, JWT authentication, automated testing, Docker, and CI/CD.

🌐 **Live API:** https://madr-api.fly.dev  
📚 **Interactive API Docs:** https://madr-api.fly.dev/docs

[![CI/CD](https://github.com/iamsaturn/madr-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/iamsaturn/madr-api/actions/workflows/deploy.yml)

---

## About the project

MADR is a backend application for managing romance books, novelists, and user accounts.

The project was developed as a backend capstone and independently implemented from a set of functional requirements, with additional focus on production-oriented practices such as authentication, database migrations, containerization, automated tests, and continuous deployment.

the API includes authentication, filtering, pagination, data validation, relational integrity, password hashing, database constraints, and automated deployment.

---

## Features

### Authentication

- User registration
- OAuth2 password flow
- JWT access tokens
- Token refresh
- Password hashing with Argon2
- Protected endpoints
- Current-user account management

### Users

- Create an account
- Retrieve authenticated user
- Update username, email, or password
- Delete account
- Duplicate username and email protection
- Username normalization

### Books

- Create books
- List books
- Retrieve a book by ID
- Update books
- Delete books
- Filter by title
- Filter by publication year
- Pagination
- Unique book titles
- Relationship with novelists

### Novelists

- Create novelists
- List novelists
- Retrieve a novelist by ID
- Update novelists
- Delete novelists
- Partial name filtering
- Pagination
- Unique novelist names
- Protection against deleting novelists that still have registered books

---

## Tech Stack

### Backend

- Python 3.14
- FastAPI
- Pydantic
- SQLAlchemy 2
- Psycopg
- PostgreSQL

### Authentication

- OAuth2
- JWT
- PyJWT
- pwdlib
- Argon2

### Database

- PostgreSQL
- Alembic
- Supabase

### Testing and code quality

- Pytest
- pytest-asyncio
- pytest-cov
- Testcontainers
- Ruff
- Poe the Poet

### Infrastructure

- Docker
- Docker Compose
- Fly.io
- GitHub Actions
- Poetry

---

## Architecture


The application uses an asynchronous SQLAlchemy session to communicate with PostgreSQL.

Database schema changes are managed through Alembic migrations.

---

## API Overview

The main API groups are:

```text
/auth
/users
/books
/novelists
```

Examples:

```http
POST /users/
POST /auth/token
POST /auth/refresh-token

GET    /users/me
PATCH  /users/me
DELETE /users/me

POST   /books/
GET    /books/
GET    /books/{book_id}
PATCH  /books/{book_id}
DELETE /books/{book_id}

POST   /novelists/
GET    /novelists/
GET    /novelists/{novelist_id}
PATCH  /novelists/{novelist_id}
DELETE /novelists/{novelist_id}
```

For the complete request and response schemas, use the interactive documentation:

**https://madr-api.fly.dev/docs**

---

## Authentication flow

Protected routes use Bearer authentication.

```text
User credentials
      │
      ▼
POST /auth/token
      │
      ▼
JWT access token
      │
      ▼
Authorization: Bearer <token>
      │
      ▼
Protected endpoint
```

The JWT subject identifies the authenticated user through their email.

Passwords are never stored directly. They are hashed before being persisted in the database.

---

## Database model

The application currently contains three main entities:

```text
User

Novelist
   │
   │ 1:N
   ▼
Book
```

A novelist can have multiple books, while every book belongs to one novelist.

Database-level uniqueness constraints protect:

- user emails
- usernames
- book titles
- novelist names

Application-level validation provides readable HTTP conflict responses before attempting invalid operations.

---

## Running locally

### Requirements

You will need:

- Python 3.14+
- Poetry
- PostgreSQL

Clone the repository:

```bash
git clone https://github.com/iamsaturn/madr-api.git
cd madr-api
```

Install the dependencies:

```bash
poetry install
```

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES=60
```

Apply database migrations:

```bash
poetry run alembic upgrade head
```

Start the development server:

```bash
poetry run poe run
```

The API will be available at:

```text
http://localhost:8000
```

Interactive documentation:

```text
http://localhost:8000/docs
```

---

## Running with Docker

The project can also run as a containerized environment.

Build and start the application and PostgreSQL:

```bash
docker compose up --build
```

Docker Compose creates:

```text
api
│
└── FastAPI container

db
│
└── PostgreSQL container
```

The API container communicates with PostgreSQL through Docker's internal network.

To stop the containers:

```bash
docker compose down
```

---

## Tests

Tests run against a real temporary PostgreSQL instance using Testcontainers rather than replacing the database layer with mocks.

Run the test suite with:

```bash
poetry run poe test
```

The test command also generates a coverage report.

Run linting with:

```bash
poetry run poe lint
```

This allows the application stack to be tested against:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

rather than testing only isolated functions.

---

## CI/CD

The repository uses GitHub Actions for continuous integration and continuous deployment.

Every push to `main` triggers the following pipeline:

```text
Push to main
      │
      ▼
Checkout repository
      │
      ▼
Set up Python
      │
      ▼
Install Poetry
      │
      ▼
Install dependencies
      │
      ▼
Ruff lint
      │
      ▼
Pytest + Testcontainers
      │
      ▼
Tests passed?
   │        │
   │ no     │ yes
   ▼        ▼
  Stop    Deploy
             │
             ▼
           Fly.io
```

A deployment is only executed when the validation job succeeds.

Production secrets are stored outside the repository and injected through the deployment environment.

---

## Deployment

The production architecture uses:

```text
GitHub
   │
   │ push
   ▼
GitHub Actions
   │
   │ CI/CD
   ▼
Fly.io
   │
   │ PostgreSQL connection
   ▼
Supabase
```

The FastAPI application runs inside a Docker container on Fly.io while the production PostgreSQL database is hosted on Supabase.

---

## Project structure

```text
madr-api/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── madr_api/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── novelists.py
│   │   └── users.py
│   │
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── settings.py
│
├── migrations/
│
├── tests/
│
├── Dockerfile
├── compose.yaml
├── entrypoint.sh
├── fly.toml
├── alembic.ini
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

## What I learned

This project was built to consolidate backend engineering concepts into a complete deployed application.

Some of the main concepts practiced include:

- REST API design
- HTTP status codes
- dependency injection with FastAPI
- request and response validation
- asynchronous database access
- ORM relationships
- database constraints
- schema migrations
- authentication and authorization
- password hashing
- JWT validation
- integration testing
- containerization
- environment configuration
- cloud deployment
- CI/CD pipelines

---

## Author

**iamsaturn**

GitHub: https://github.com/iamsaturn
