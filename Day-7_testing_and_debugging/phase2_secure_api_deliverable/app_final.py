"""Corrected reference Customer API for Phase 2 training."""
import os
import sqlite3
from typing import Any
import jwt
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field

app = FastAPI(title="Phase 2 Corrected Customer API")

JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET must be configured securely at runtime")
EXPECTED_ISSUER = os.environ.get("JWT_ISSUER", "phase2-training-issuer")
EXPECTED_AUDIENCE = os.environ.get("JWT_AUDIENCE", "customer-api")
DB_PATH = os.environ.get("DB_PATH", "customers_final.db")

class Customer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=120)

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL,
        age INTEGER NOT NULL CHECK(age >= 0 AND age <= 120), status TEXT NOT NULL)""")
    cur.execute("SELECT COUNT(*) FROM customers")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", [
            (101, "Alice", "alice@example.com", 28, "active"),
            (102, "Bob", "bob@example.com", 35, "active"),
            (103, "Charlie", "charlie@example.com", 44, "inactive"),
        ])
    conn.commit()
    conn.close()

init_db()

def get_current_user(authorization: str | None) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        return jwt.decode(
            token, JWT_SECRET, algorithms=["HS256"],
            issuer=EXPECTED_ISSUER, audience=EXPECTED_AUDIENCE,
            options={"require": ["sub", "iss", "aud", "exp"]},
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def authorize_customer_access(user: dict[str, Any], customer_id: int):
    if user.get("role") == "admin":
        return
    if str(user["sub"]) != str(customer_id):
        raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int, authorization: str | None = Header(default=None)):
    user = get_current_user(authorization)
    authorize_customer_access(user, customer_id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,age,status FROM customers WHERE id=?", (customer_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": row[0], "name": row[1], "email": row[2], "age": row[3], "status": row[4]}

@app.post("/customers")
def create_customer(customer: Customer, authorization: str | None = Header(default=None)):
    user = get_current_user(authorization)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can create customers")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name,email,age,status) VALUES (?,?,?,?)",
                (customer.name, str(customer.email), customer.age, "active"))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, **customer.model_dump(mode="json")}

@app.get("/debug")
def debug():
    # No credentials are exposed.
    return {"environment": os.getenv("ENVIRONMENT", "development")}
