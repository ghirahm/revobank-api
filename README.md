# REVOBANK API

## Overview

REVOBANK API is a secure, Flask-based banking API that allows users to register, log in, manage accounts, perform transactions, and handle basic banking operations. The system uses JWT (JSON Web Tokens) for authentication and connects to a SQLite database for lightweight, file-based storage—ideal for development or small-scale deployments.

---

## Features

- User registration & login with JWT authentication
- Account creation and retrieval
- Deposit, withdrawal, and transfer transactions
- RESTful API with clear request/response structure
- Built-in ownership checks to ensure users can only access their data

## Tech Stack

- Backend: Flask
- Database: SQLite
- Auth: JWT (flask-jwt-extended)
- ORM: SQLAlchemy
- Migrations: Flask-Migrate

## Database Schema and Relationships

The application consists of three main models:

### 1. **User**

| Field         | Type     | Description              |
| ------------- | -------- | ------------------------ |
| id            | Integer  | Primary key              |
| username      | String   | Unique                   |
| email         | String   | Unique                   |
| password_hash | String   | Hashed password          |
| created_at    | DateTime | Timestamp of creation    |
| updated_at    | DateTime | Timestamp of last update |

### 2. **Account**

| Field          | Type     | Description              |
| -------------- | -------- | ------------------------ |
| id             | Integer  | Primary key              |
| user_id        | Integer  | Foreign key → User.id    |
| account_type   | String   | e.g., savings, checking  |
| account_number | String   | Unique account number    |
| balance        | Float    | Account balance          |
| created_at     | DateTime | Timestamp of creation    |
| updated_at     | DateTime | Timestamp of last update |

### 3. **Transaction**

| Field           | Type     | Description                               |
| --------------- | -------- | ----------------------------------------- |
| id              | Integer  | Primary key                               |
| type            | String   | 'deposit', 'withdrawal', 'transfer'       |
| amount          | Float    | Transaction amount                        |
| from_account_id | Integer  | FK → Account.id (nullable for deposit)    |
| to_account_id   | Integer  | FK → Account.id (nullable for withdrawal) |
| description     | String   | Optional note                             |
| created_at      | DateTime | Timestamp of creation                     |

### Relationships

- A **User** can have multiple **Accounts**.
- A **Transaction** may involve one or two **Accounts**, depending on type.

---

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///revobank.db
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

### 3. Initialize the Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## API Endpoints

### 🔐 Auth

#### Register User

```http
POST /register
```

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Login User

```http
POST /login
```

```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}
```

---

### 👤 User

> All routes below require `Authorization: Bearer <access_token>`

#### Get User Details

```http
GET /users/<id>
```

#### Update User

```http
PUT /users/<id>
```

#### Delete User

```http
DELETE /users/<id>
```

---

### 💳 Account

#### Create Account

```http
POST /accounts
```

```json
{
  "account_type": "savings"
}
```

#### Get Account

```http
GET /accounts/<account_id>
```

---

### 💸 Transactions

#### Deposit

```http
POST /transactions
```

```json
{
  "type": "deposit",
  "amount": 500.0,
  "to_account_id": 1
}
```

#### Transfer

```http
POST /transactions
```

```json
{
  "type": "transfer",
  "amount": 200.0,
  "from_account_id": 1,
  "to_account_id": 2
}
```

---

## Authorization Logic

- JWT tokens are used to verify user identity.
- Users can only access or modify their own accounts and transactions.
- Identity is extracted from the JWT payload and checked against request targets.

---

## Postman & API Reference

📘 **API Documentation**: [Postman Docs](https://documenter.getpostman.com/view/28293786/2sAYkBrLvZ)

Online API [REVOBANK API](https://revobankapi.skycast.site/users/1)
