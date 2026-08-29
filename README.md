# MADR API — Modern Archive for Digital Romance

A production-ready REST API for managing romance books and novelists, built with FastAPI, PostgreSQL, JWT authentication, automated testing, Docker, and CI/CD.

🌐 **Live API:** https://madr-api.fly.dev  
📚 **API Docs:** https://madr-api.fly.dev/docs  
🖥️ **Live Demo:** https://madr-web.fly.dev

[![CI/CD](https://github.com/iamsaturn/madr-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/iamsaturn/madr-api/actions/workflows/deploy.yml)

![MADR Streamlit demo](docs/madr-demo.gif)

## About

MADR is a backend capstone project independently implemented from a set of functional requirements. It provides a REST API for books, novelists, and user accounts, with authentication, relational data, filtering, pagination, and automated deployment.

A minimal Streamlit client is included to demonstrate the deployed API being consumed by a real interface.

## Features

- User registration and account management
- OAuth2 authentication with JWT access and refresh tokens
- Argon2 password hashing
- CRUD operations for books and novelists
- Filtering and pagination
- PostgreSQL relational integrity and uniqueness constraints
- Alembic database migrations
- Async SQLAlchemy
- Integration tests with Testcontainers
- Dockerized development and deployment
- CI/CD with GitHub Actions
- Minimal Streamlit client

## Tech Stack

**Backend:** Python 3.14, FastAPI, Pydantic, SQLAlchemy, Psycopg  
**Database:** PostgreSQL, Alembic, Supabase  
**Security:** OAuth2, JWT, PyJWT, pwdlib, Argon2  
**Testing:** Pytest, pytest-asyncio, Testcontainers, pytest-cov, Ruff  
**Infrastructure:** Docker, Docker Compose, Fly.io, GitHub Actions, Poetry  
**Frontend demo:** Streamlit, Requests

## Architecture

```text
Streamlit client
      │ HTTP
      ▼
FastAPI · Fly.io
      │
  SQLAlchemy
      │
      ▼
PostgreSQL · Supabase
```

Books and novelists can be browsed without authentication. Write operations and account management require a Bearer JWT.

## API

Main route groups:

```text
/auth
/users
/books
/novelists
```

Example endpoints:

```http
POST   /auth/token
POST   /auth/refresh-token

POST   /users/
GET    /users/me
PATCH  /users/me
DELETE /users/me

GET    /books/
POST   /books/
PATCH  /books/{book_id}
DELETE /books/{book_id}

GET    /novelists/
POST   /novelists/
PATCH  /novelists/{novelist_id}
DELETE /novelists/{novelist_id}
```

Full schemas and interactive testing are available at **https://madr-api.fly.dev/docs**.

## Running locally

```bash
git clone https://github.com/iamsaturn/madr-api.git
cd madr-api
poetry install
```

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES=60
```

Run migrations and start the API:

```bash
poetry run alembic upgrade head
poetry run poe run
```

Or run the containerized environment:

```bash
docker compose up --build
```

## Tests

The backend suite runs against a temporary real PostgreSQL instance using Testcontainers.

```bash
poetry run poe lint
poetry run poe test
```

**53 tests · 98% coverage**

## CI/CD

Every push to `main` runs:

```text
Lint + Tests
     ↓
Deploy API
     ↓
API smoke test
     ↓
Deploy Streamlit client
```

The API and Streamlit client run on Fly.io, while the production PostgreSQL database is hosted on Supabase.

## Author

**iamsaturn** · https://github.com/iamsaturn
