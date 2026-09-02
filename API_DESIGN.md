# API Design

## Project
AI-Powered Customer Support Ticket Tracking System

## 1. Entities

### User
Represents a person using the system.

Fields:
- id
- name
- email
- password
- role

Roles:
- CUSTOMER
- AGENT
- ADMIN

### Ticket
Represents a customer support request.

Fields:
- id
- title
- description
- status
- priority
- category
- customer_id
- assigned_agent_id
- created_at
- updated_at

### AI Analysis
Stores AI-generated analysis for a support ticket.

Fields:
- id
- ticket_id
- category
- priority
- sentiment
- suggested_response

## 2. Ticket Status

- OPEN
- IN_PROGRESS
- RESOLVED
- CLOSED

## 3. Ticket Priority

- LOW
- MEDIUM
- HIGH
- CRITICAL

## 4. Relationships

- A Customer can create multiple Tickets.
- A Ticket belongs to one Customer.
- A Support Agent can be assigned multiple Tickets.
- A Ticket can be assigned to one Support Agent.
- A Ticket can have an AI Analysis.
- An AI Analysis belongs to one Ticket.

## 5. Entity Relationship Overview

User (Customer)
    |
    | creates
    v
Ticket
    |
    | analyzed by
    v
AI Analysis

User (Support Agent)
    |
    | assigned to
    v
Ticket
## 6. REST Endpoint Plan

### User Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /users | Create a new user |
| GET | /users/{user_id} | Get user details |

### Ticket Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /tickets | Create a support ticket |
| GET | /tickets | Get all tickets |
| GET | /tickets/{ticket_id} | Get a specific ticket |
| PUT | /tickets/{ticket_id} | Update a ticket |
| DELETE | /tickets/{ticket_id} | Delete a ticket |

### AI Analysis Endpoint

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /tickets/{ticket_id}/analyze | Analyze a ticket using AI |

## 7. Success and Error Cases

### Success Responses

- 200 OK – Request completed successfully.
- 201 Created – Resource created successfully.
- 204 No Content – Resource deleted successfully.

### Error Responses

- 400 Bad Request – Invalid request data.
- 401 Unauthorized – Authentication is required.
- 403 Forbidden – User does not have permission.
- 404 Not Found – Requested resource does not exist.
- 409 Conflict – Resource already exists or conflicts with existing data.
- 422 Unprocessable Entity – Request validation failed.
- 500 Internal Server Error – Unexpected server error.