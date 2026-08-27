# Phase 1 Deliverable — Deliberately Broken Customer API

## Objective
Test, debug, fix, and document a deliberately broken REST API using:
Unit tests, integration tests, mocks, API tests, coverage, debugging, logging, and RCA.

## Setup
pip install -r requirements.txt

## Run tests
pytest -v

Expected initially:
- Active customer: PASS
- Inactive customer: PASS
- Missing customer: FAIL

## Coverage
pytest --cov=. --cov-report=term-missing

## Run API
uvicorn app:app --reload

Try:
GET /customers/101
GET /customers/102
GET /customers/999

## Deliberate defect
A non-existent customer incorrectly returns HTTP 200 with status "inactive".
Expected contract:
- Existing customer -> 200
- Missing customer -> 404

## Expected fix
Replace the missing-customer branch with:
raise HTTPException(status_code=404, detail="Customer Not Found")

Then rerun tests and coverage.

## RCA
Use RCA_TEMPLATE.md to document:
incident, impact, evidence, immediate cause, root cause,
contributing factors, corrective action, preventive action, validation.
