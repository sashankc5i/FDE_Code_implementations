employees = {
    "EMP001": {
        "employee_id": "EMP001",
        "name": "Sashank",
        "department": "Data Engineering",
        "manager_id": "MGR001",
    },
    "EMP002": {
        "employee_id": "EMP002",
        "name": "Rahul",
        "department": "Finance",
        "manager_id": "MGR002",
    },
}


reimbursements = {
    "CLM1001": {
        "claim_id": "CLM1001",
        "employee_id": "EMP001",
        "expense_type": "Travel",
        "amount": 8500.0,
        "description": "Client visit travel",
        "status": "PENDING",
    },
    "CLM1002": {
        "claim_id": "CLM1002",
        "employee_id": "EMP002",
        "expense_type": "Food",
        "amount": 2500.0,
        "description": "Client meeting dinner",
        "status": "PENDING",
    },
}


reimbursement_policy = {
    "standard_limit": 5000.0,
    "requires_manager_review_above": 5000.0,
    "supported_expenses": [
        "Travel",
        "Food",
        "Accommodation",
    ],
}