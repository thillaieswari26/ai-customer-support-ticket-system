# AI-Powered Customer Support Ticket Tracking System

A FastAPI backend for managing customer support tickets with JWT authentication, PostgreSQL, ticket search and filtering, and AI-powered ticket analysis.

## Features

- JWT-based authentication
- Secure password hashing
- Create, read, update, and delete tickets
- Ticket ownership authorization
- Ticket search and filtering
- Pagination
- AI-powered ticket analysis
- AI service failure handling
- PostgreSQL database
- Async SQLAlchemy
- Alembic database migrations
- Automated API tests
- OpenAPI/Swagger documentation
- Structured logging and error handling

## Tech Stack

- Python 3.13+
- FastAPI
- PostgreSQL
- SQLAlchemy
- asyncpg
- Alembic
- JWT
- bcrypt
- Pytest
- HTTPX

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/thillaieswari26/ai-customer-support-ticket-system.git
cd ai-customer-support-ticket-system
2. Create a virtual environment

Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root.

Example:

DATABASE_URL=postgresql+asyncpg://postgres@localhost:5432/customer_support_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Do not commit the .env file to GitHub.

Database Setup

Create the PostgreSQL database:

createdb -U postgres customer_support_db

Run the Alembic migrations:

alembic upgrade head

To roll back the latest migration:

alembic downgrade -1
Run the API

Start the FastAPI development server:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000
API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

OpenAPI schema:

http://127.0.0.1:8000/openapi.json
Authentication
Login
POST /auth/login

Example request:

{
  "email": "user@example.com",
  "password": "your-password"
}

The response contains a JWT access token.

Use the token in protected endpoints:

Authorization: Bearer <access_token>
Ticket Endpoints
Create Ticket
POST /tickets

Example:

{
  "title": "Unable to login",
  "description": "I cannot access my account.",
  "priority": "HIGH",
  "category": "TECHNICAL"
}
List Tickets
GET /tickets

Supported query parameters:

search
status_filter
priority
category
skip
limit

Example:

GET /tickets?search=login&priority=HIGH&limit=10
Get Ticket
GET /tickets/{ticket_id}

Example:

GET /tickets/1
Update Ticket
PUT /tickets/{ticket_id}

Example:

{
  "title": "Updated login issue",
  "priority": "MEDIUM"
}
Delete Ticket
DELETE /tickets/{ticket_id}

Example:

DELETE /tickets/1
AI Ticket Analysis

Analyze a ticket using the AI service:

POST /tickets/{ticket_id}/analyze

Example:

POST /tickets/1/analyze

The analysis provides:

Category
Priority
Sentiment
Suggested response

If the AI service fails, the API returns:

503 Service Unavailable
Running Tests

The project uses an isolated PostgreSQL test database.

Run all tests:

pytest -v

The test suite covers:

Ticket creation
Validation failures
Ticket listing
Ticket retrieval
Ticket updates
Ticket deletion
Authorization boundaries
AI service failures
Database Migration Commands

Create a new migration:

alembic revision --autogenerate -m "describe migration"

Apply migrations:

alembic upgrade head

Rollback the latest migration:

alembic downgrade -1
Project Structure
ai-customer-support-ticket-system/
│
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic/
├── tests/
├── .env
├── .env.example
├── alembic.ini
├── requirements.txt
├── check_db.py
└── README.md
Security
Passwords are stored using secure hashing.
Protected endpoints require JWT authentication.
Users can only access their own tickets.
Secrets and environment-specific configuration should be stored in .env.
.env should never be committed to the repository.
License

This project was developed as part of a backend AI engineering internship project.


Save the file.

Then run:

```powershell id="h7q4px"
git status