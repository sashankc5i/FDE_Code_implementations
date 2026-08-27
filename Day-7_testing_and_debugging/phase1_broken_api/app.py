from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("customer-api")

app = FastAPI(title="Phase 1 Broken Customer API")

CUSTOMERS = {
    101: {"customer_id": 101, "status": "active", "name": "Alice"},
    102: {"customer_id": 102, "status": "inactive", "name": "Bob"},
}

class Customer(BaseModel):
    customer_id: int
    status: str
    name: str

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    logger.info("customer lookup customer_id=%s", customer_id)
    customer = CUSTOMERS.get(customer_id)

    # DELIBERATE BUG:
    # A missing customer is incorrectly represented as an inactive customer.
    if customer is None:
        logger.warning("customer not found customer_id=%s", customer_id)
        return {
            "customer_id": customer_id,
            "status": "inactive",
            "name": "Unknown",
        }

    return customer
