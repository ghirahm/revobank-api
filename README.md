# REVOBANK API

## Overview
This is a Flask-based banking API that allows users to manage accounts, create transactions, and perform basic banking operations. The application connects to a SQLITE database and provides a RESTful API for interacting with user accounts and transactions.

---

## Database Schema and Relationships

The application consists of three main models:

### 1. **User**
- `id` (Primary Key, Integer)
- `username` (String, Unique)
- `email` (String, Unique)
- `password_hash` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### 2. **Account**
- `id` (Primary Key, Integer)
- `user_id` (Foreign Key → User.id)
- `account_type` (String)
- `account_number` (String, Unique)
- `balance` (Float)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### 3. **Transaction**
- `id` (Primary Key, Integer)
- `type` (String: 'deposit', 'withdrawal', 'transfer')
- `amount` (Float)
- `from_account_id` (Foreign Key → Account.id, Nullable)
- `to_account_id` (Foreign Key → Account.id, Nullable)
- `description` (String, Optional)
- `created_at` (DateTime)

#### **Relationships**
- A **User** can have multiple **Accounts**.
- A **Transaction** can involve one or two **Accounts** (for withdrawals, deposits, or transfers).

---

## Connecting the Application to the Database

### **1. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **2. Configure Environment Variables**
Create a `.env` file in the root directory with the following:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/banking_db
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

### **3. Initialize Database**
Run the following commands to create tables:
```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## API Endpoints and Database Operations

### **1. Creating a User**
```sh
POST /users
```
**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword"
}
```
**Response:**
```json
{
    "message": "User created successfully",
    "user_id": 1
}
```

### **2. Creating an Account**
```sh
POST /accounts
```
**Request Body:**
```json
{
    "user_id": 1,
    "account_type": "savings",
    "account_number": "1234567890",
    "balance": 1000.00
}
```

### **3. Initiating a Transaction**
```sh
POST /transactions
```
**Deposit Example:**
```json
{
    "type": "deposit",
    "amount": 500.00,
    "to_account_id": 1
}
```
**Transfer Example:**
```json
{
    "type": "transfer",
    "amount": 200.00,
    "from_account_id": 1,
    "to_account_id": 2
}
```

### **4. Getting Account Details**
```sh
GET /accounts/1
```
**Response:**
```json
{
    "id": 1,
    "user_id": 1,
    "account_type": "savings",
    "account_number": "1234567890",
    "balance": 1300.00,
    "created_at": "2025-03-28 10:00:00",
    "updated_at": "2025-03-28 12:00:00"
}
```

---

Full Documentation of API is Available on
Test of Applicaitons is on 
