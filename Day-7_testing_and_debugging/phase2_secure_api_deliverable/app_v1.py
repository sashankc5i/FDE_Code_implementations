"""Deliberately vulnerable Customer API for Phase 2 training."""
import os
import sqlite3
import jwt
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Phase 2 Vulnerable Customer API")

# VULNERABILITY: hardcoded secrets
JWT_SECRET = "training-secret-123"
DATABASE_PASSWORD = "admin123"
DB_PATH = "customers.db"

class Customer(BaseModel):
    name: str
    email: str
    age: int

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER, status TEXT)""")
    cur.execute("DELETE FROM customers")
    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", [
        (101, "Alice", "alice@example.com", 28, "active"),
        (102, "Bob", "bob@example.com", 35, "active"),
        (103, "Charlie", "charlie@example.com", 44, "inactive"),
    ])
    conn.commit()
    conn.close()

init_db()

# VULNERABILITY: signature verification disabled
def get_current_user(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.replace("Bearer ", "")
    return jwt.decode(token, options={"verify_signature": False})

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int, authorization: str | None = Header(default=None)):
    user = get_current_user(authorization)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,age,status FROM customers WHERE id=?", (customer_id,))
    row = cur.fetchone()
    conn.close()

    # VULNERABILITY: nonexistent customer incorrectly returns inactive
    if not row:
        return {"id": customer_id, "status": "inactive"}

    # VULNERABILITY: BOLA/IDOR; no resource ownership check
    return {"id": row[0], "name": row[1], "email": row[2], "age": row[3],
            "status": row[4], "requested_by": user.get("sub")}

@app.post("/customers")
def create_customer(customer: Customer, authorization: str | None = Header(default=None)):
    get_current_user(authorization)

    # VULNERABILITY: insufficient business/input validation
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name,email,age,status) VALUES (?,?,?,?)",
                (customer.name, customer.email, customer.age, "active"))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, **customer.model_dump()}

@app.get("/debug")
def debug():
    # VULNERABILITY: secrets exposed through API
    return {"environment": os.getenv("ENVIRONMENT", "development"),
            "database_password": DATABASE_PASSWORD,
            "jwt_secret": JWT_SECRET}
