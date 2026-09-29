from data import employees, reimbursements, reimbursement_policy


def get_employee(employee_id: str) -> dict:
    """Retrieve employee information."""

    employee = employees.get(employee_id)

    if not employee:
        return {
            "success": False,
            "error": f"Employee {employee_id} not found",
        }

    return {
        "success": True,
        "employee": employee,
    }


def get_reimbursement(claim_id: str) -> dict:
    """Retrieve reimbursement information."""

    claim = reimbursements.get(claim_id)

    if not claim:
        return {
            "success": False,
            "error": f"Claim {claim_id} not found",
        }

    return {
        "success": True,
        "claim": claim,
    }


def create_reimbursement(
    employee_id: str,
    expense_type: str,
    amount: float,
    description: str,
) -> dict:
    """Create a new reimbursement claim."""

    if employee_id not in employees:
        return {
            "success": False,
            "error": f"Employee {employee_id} not found",
        }

    if amount <= 0:
        return {
            "success": False,
            "error": "Amount must be greater than zero",
        }

    if expense_type not in reimbursement_policy["supported_expenses"]:
        return {
            "success": False,
            "error": f"Unsupported expense type: {expense_type}",
        }

    claim_id = f"CLM{len(reimbursements) + 1001}"

    claim = {
        "claim_id": claim_id,
        "employee_id": employee_id,
        "expense_type": expense_type,
        "amount": amount,
        "description": description,
        "status": "PENDING",
    }

    reimbursements[claim_id] = claim

    return {
        "success": True,
        "claim": claim,
    }


def approve_reimbursement(
    claim_id: str,
    approver_id: str,
) -> dict:
    """Approve a pending reimbursement claim."""

    claim = reimbursements.get(claim_id)

    if not claim:
        return {
            "success": False,
            "error": f"Claim {claim_id} not found",
        }

    if claim["status"] == "APPROVED":
        return {
            "success": True,
            "message": f"Claim {claim_id} is already approved",
            "claim": claim,
        }

    if claim["status"] != "PENDING":
        return {
            "success": False,
            "error": (
                f"Claim {claim_id} cannot be approved "
                f"because its status is {claim['status']}"
            ),
        }

    claim["status"] = "APPROVED"
    claim["approved_by"] = approver_id

    return {
        "success": True,
        "message": f"Claim {claim_id} approved",
        "claim": claim,
    }


def reject_reimbursement(
    claim_id: str,
    approver_id: str,
    reason: str,
) -> dict:
    """Reject a pending reimbursement claim."""

    claim = reimbursements.get(claim_id)

    if not claim:
        return {
            "success": False,
            "error": f"Claim {claim_id} not found",
        }

    if claim["status"] == "REJECTED":
        return {
            "success": True,
            "message": f"Claim {claim_id} is already rejected",
            "claim": claim,
        }

    if claim["status"] != "PENDING":
        return {
            "success": False,
            "error": (
                f"Claim {claim_id} cannot be rejected "
                f"because its status is {claim['status']}"
            ),
        }

    claim["status"] = "REJECTED"
    claim["rejected_by"] = approver_id
    claim["rejection_reason"] = reason

    return {
        "success": True,
        "message": f"Claim {claim_id} rejected",
        "claim": claim,
    }