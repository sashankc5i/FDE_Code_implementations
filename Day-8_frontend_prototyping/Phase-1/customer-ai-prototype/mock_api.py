from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Customer Mock API")


# -----------------------------
# Sample customer data
# -----------------------------

CUSTOMERS = {
    101: {
        "customer_id": 101,
        "name": "Customer 101",
        "status": "active",
        "segment": "Enterprise",
        "region": "West"
    },
    102: {
        "customer_id": 102,
        "name": "Customer 102",
        "status": "inactive",
        "segment": "SMB",
        "region": "South"
    },
    103: {
        "customer_id": 103,
        "name": "Customer 103",
        "status": "active",
        "segment": "Enterprise",
        "region": "North"
    }
}


# -----------------------------
# Customer lookup API
# -----------------------------

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):

    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer