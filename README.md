# User Management API

A RESTful User Management API built with Flask, MySQL, and SQLAlchemy.

This project was developed as part of a Software Engineer assignment.

---

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- MySQL
- PyMySQL
- python-dotenv
- Git & GitHub

---

## Features

- Create a new user
- Retrieve all users
- Retrieve a user by ID
- Search users by name or email
- Pagination
- Required field validation
- Email format validation
- Duplicate email handling
- User-not-found handling
- Database error handling
- JSON API responses
- Modular architecture
- Environment-based configuration

---

## Project Structure

```text
user-management-api/
│
├── models/
│   ├── __init__.py
│   └── user.py
│
├── routes/
│   ├── __init__.py
│   └── user_routes.py
│
├── services/
│   ├── __init__.py
│   └── user_service.py
│
├── app.py
├── config.py
├── .gitignore
├── requirements.txt
└── README.md
```

> `.env` is used for local environment configuration and is excluded from version control using `.gitignore`.

---

# Database

## Database

```text
users
```

## Users Table

| Column | Type | Constraints |
|---|---|---|
| id | INT | Primary Key |
| name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(150) | UNIQUE, NOT NULL |
| role | VARCHAR(50) | NOT NULL |

The application uses SQLAlchemy to create the database table when the application is initialized.

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/vikashsingh73559-dot/user-management-api.git
cd user-management-api
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Create MySQL Database

Create a MySQL database named:

```text
users
```

Make sure MySQL is running before starting the application.

## 6. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://root:@localhost/users
SECRET_KEY=your-secret-key-here
```

If your MySQL installation uses a password, update the connection string accordingly.

> Never commit the `.env` file to GitHub.

## 7. Run the Application

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

# API Documentation

## 1. Get All Users

### Endpoint

```http
GET /users
```

### Example

```text
http://127.0.0.1:5000/users
```

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Vikash Singh",
      "email": "vikash@example.com",
      "role": "Software Engineer"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "pages": 1
  }
}
```

### Status

```text
200 OK
```

---

## 2. Create User

### Endpoint

```http
POST /users
```

### Request Body

```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "role": "Developer"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "role": "Developer"
  }
}
```

### Status

```text
201 Created
```

---

## 3. Get User by ID

### Endpoint

```http
GET /users/<id>
```

### Example

```text
http://127.0.0.1:5000/users/1
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Vikash Singh",
    "email": "vikash@example.com",
    "role": "Software Engineer"
  }
}
```

### Status

```text
200 OK
```

---

## 4. Search Users

Users can be searched by name or email.

### Endpoint

```http
GET /users?search=<search_term>
```

### Example

```text
http://127.0.0.1:5000/users?search=vikash
```

The search checks both `name` and `email`.

---

## 5. Pagination

### Endpoint

```http
GET /users?page=1&limit=10
```

### Example

```text
http://127.0.0.1:5000/users?page=1&limit=10
```

### Response

```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 0,
    "pages": 0
  }
}
```

### Default Values

| Parameter | Default |
|---|---:|
| page | 1 |
| limit | 10 |

---

# Validation & Error Handling

## Missing Required Field

Required fields:

- `name`
- `email`
- `role`

### Example

```json
{
  "name": "Rahul",
  "email": "rahul@example.com"
}
```

### Response

```json
{
  "success": false,
  "error": "role is required"
}
```

### Status

```text
400 Bad Request
```

---

## Invalid Email

### Example

```json
{
  "name": "Rahul",
  "email": "invalid-email",
  "role": "Developer"
}
```

### Response

```json
{
  "success": false,
  "error": "Invalid email format"
}
```

### Status

```text
400 Bad Request
```

---

## Duplicate Email

If the submitted email already exists:

```json
{
  "success": false,
  "error": "Email already exists"
}
```

### Status

```text
409 Conflict
```

---

## User Not Found

### Example

```text
GET /users/999
```

### Response

```json
{
  "success": false,
  "error": "User not found"
}
```

### Status

```text
404 Not Found
```

---

# API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | Retrieve users |
| POST | `/users` | Create a user |
| GET | `/users/<id>` | Retrieve user by ID |
| GET | `/users?search=` | Search by name/email |
| GET | `/users?page=1&limit=10` | Paginated users |

---

# Architecture

The application follows a modular architecture:

```text
Client
   │
   ▼
Routes
   │
   ▼
Services
   │
   ▼
Models
   │
   ▼
MySQL
```

### Routes

Responsible for:

- Handling HTTP requests
- Request validation
- Query parameters
- HTTP responses

### Services

Responsible for:

- User-related business logic
- Database operations
- Query and pagination logic

### Models

Responsible for:

- Database schema
- Database fields
- Data serialization

This separation keeps the application maintainable and makes it easier to extend.

---

# Assumptions

- MySQL is running locally during development.
- The local MySQL `root` user does not have a password.
- User email addresses must be unique.
- `name`, `email`, and `role` are required.
- API responses are JSON-based.
- Pagination defaults to page 1 with a limit of 10.
- Search supports both name and email.
- The `.env` file contains local configuration and is excluded from Git.
- The API is intended for local development as part of the assignment.

---

# Git Workflow

The assignment implementation was developed using a dedicated branch:

```text
main
  │
  └── assignment
```

The `assignment` branch contains the implementation and documentation changes.

A Pull Request is created from:

```text
assignment → main
```

---

# Testing

The API was tested locally using Postman.

The following scenarios were tested:

- Create user
- Retrieve all users
- Retrieve user by ID
- Search users
- Pagination
- Missing required fields
- Invalid email format
- Duplicate email
- User not found
- MySQL database integration

---

# AI Usage Declaration

AI tools were used during development of this assignment.

## AI Tool

- ChatGPT

## AI-Assisted Areas

AI assistance was used for:

- Project structure suggestions
- Flask API implementation guidance
- SQLAlchemy model structure
- Validation and error-handling guidance
- Search and pagination implementation
- Debugging and troubleshooting
- README documentation drafting

## Manual Work

The implementation was manually reviewed, modified, tested, and integrated.

The developer understands the implementation and can explain:

- API architecture
- Flask routes
- Service layer
- SQLAlchemy models
- MySQL integration
- Validation logic
- Pagination
- Error handling
- Git workflow

---

# Future Improvements

For a production environment, the following improvements could be considered:

- JWT authentication
- Role-based authorization
- Automated unit and integration tests
- Database migrations
- Docker containerization
- API rate limiting
- Structured logging
- Monitoring and health checks
- CI/CD pipeline
- Production database configuration