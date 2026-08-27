PHASE 2 DELIVERABLE — SECURE SOFTWARE DEVELOPMENT

app_v1.py
----------
Deliberately vulnerable version. Start here. Investigate before looking at app_final.py.

app_final.py
------------
Corrected reference implementation. Use only after completing your own investigation.

README
------
Install:
  pip install fastapi uvicorn PyJWT "pydantic[email]"

Run vulnerable API:
  uvicorn app_v1:app --reload

Run corrected API (PowerShell):
  $env:JWT_SECRET="secure-training-value"
  uvicorn app_final:app --reload

Run corrected API (Linux/macOS):
  export JWT_SECRET="secure-training-value"
  uvicorn app_final:app --reload

Dependency scan:
  pip-audit

Training scope:
- Input validation
- Authentication/JWT validation
- Authorization/BOLA
- Secret exposure
- HTTP error handling
- Dependency scanning
- Security regression testing

Do not deploy either training implementation as a production identity/security platform.
