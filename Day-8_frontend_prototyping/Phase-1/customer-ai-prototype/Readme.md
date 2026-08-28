# `README.md`


# 🤖 Customer AI Assistant

A rapid AI prototype that demonstrates how an existing Customer REST API can be exposed through a simple Streamlit-based user interface.

The project uses a **FastAPI mock backend** to simulate the Customer API, allowing the frontend and user experience to be developed without depending on a production backend.

---

## 📌 Project Overview

The purpose of this project is to demonstrate a rapid-prototyping approach for an AI-assisted customer application.

The prototype allows an operations user to:

1. Enter a Customer ID.
2. Ask a natural-language question.
3. Retrieve customer information through a REST API.
4. Display customer information in the UI.
5. Generate a simple AI-style operational response.
6. Handle common API and user-input failures gracefully.

The project intentionally uses **sample customer data and a mock API** rather than production systems.

> **The goal is to validate the user experience and integration workflow, not to build a production AI platform.**

---

# 🎯 Objectives

The prototype demonstrates the following concepts:

- Rapid UI development using Streamlit
- REST API integration
- HTTP communication
- JSON data exchange
- Mock API development using FastAPI
- API contract thinking
- Error handling
- User journey validation
- AI-assisted response generation
- Separation between frontend and backend dependencies
- Prototype → production transition planning

---

# 🏗️ Architecture

The current prototype architecture is:

```text
                    Operations User
                           |
                           v
                   +----------------+
                   |  Streamlit UI  |
                   +----------------+
                           |
                           | HTTP GET
                           v
                   +----------------+
                   |  FastAPI Mock   |
                   |      API        |
                   +----------------+
                           |
                           v
                   +----------------+
                   | Sample Customer |
                   |      Data       |
                   +----------------+
                           |
                           | JSON
                           v
                   +----------------+
                   | Response Logic |
                   +----------------+
                           |
                           v
                   +----------------+
                   |  Streamlit UI  |
                   +----------------+
````

---

# 🧩 Technology Stack

| Component   | Technology | Purpose                         |
| ----------- | ---------- | ------------------------------- |
| Frontend    | Streamlit  | Rapid application UI            |
| Backend     | FastAPI    | Mock REST API                   |
| HTTP Client | Requests   | API communication               |
| Data Format | JSON       | Request/response representation |
| Server      | Uvicorn    | Runs FastAPI                    |
| Language    | Python     | Application implementation      |

---

# 📁 Project Structure

```text
customer-ai-prototype/
│
├── app.py
├── mock_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `app.py`

Contains the Streamlit application.

Responsibilities:

* User input
* Customer ID selection
* Question input
* HTTP communication
* API response processing
* UI rendering
* Error handling
* AI-style response generation

### `mock_api.py`

Contains the FastAPI mock Customer API.

Responsibilities:

* Simulate Customer API
* Provide sample customer data
* Return JSON responses
* Return appropriate HTTP status codes

### `requirements.txt`

Contains Python dependencies required to run the project.

### `.gitignore`

Prevents local environments, secrets, caches, logs and other unnecessary files from being committed to Git.

---

# 🔌 API Contract

The prototype exposes the following endpoint:

```http
GET /customers/{customer_id}
```

## Successful Request

Example:

```http
GET /customers/101
```

Response:

```json
{
    "customer_id": 101,
    "name": "Customer 101",
    "status": "active",
    "segment": "Enterprise",
    "region": "West"
}
```

HTTP status:

```text
200 OK
```

---

## Customer Not Found

Example:

```http
GET /customers/999
```

Response:

```json
{
    "detail": "Customer not found"
}
```

HTTP status:

```text
404 Not Found
```

### Important Business Rule

A customer that does not exist must **not** be treated as an inactive customer.

```text
Customer exists
      |
      +-- Active   → 200
      |
      +-- Inactive → 200

Customer does not exist
      |
      +-- 404 Not Found
```

---

# 👤 User Journey

The primary user journey is:

```text
Operations User
      |
      v
Open Customer AI Assistant
      |
      v
Enter Customer ID
      |
      v
Ask a Question
      |
      v
Streamlit sends HTTP request
      |
      v
Mock Customer API
      |
      v
Retrieve Customer Data
      |
      v
Generate Operational Response
      |
      v
Display Result
      |
      v
User Takes Action
```

---

# 🖥️ Prototype UI

The application provides:

```text
+--------------------------------------+
|       Customer AI Assistant          |
+--------------------------------------+
|                                      |
| Customer ID                          |
| [ 101 ]                              |
|                                      |
| Ask a question                       |
| [ What is the status...? ]           |
|                                      |
|              [ Ask AI ]              |
|                                      |
+--------------------------------------+
| Customer Information                 |
|                                      |
| Customer ID: 101                     |
| Status: ACTIVE                       |
| Name: Customer 101                   |
| Segment: Enterprise                  |
| Region: West                         |
|                                      |
+--------------------------------------+
| AI Response                          |
|                                      |
| Customer 101 is currently active...  |
+--------------------------------------+
```

The UI is intentionally minimal because the objective is to validate the **core user journey** rather than build a complete production interface.

---

# 🚀 Getting Started

## Prerequisites

You need:

* Python 3.x
* pip
* A terminal/command prompt

It is recommended to use a Python virtual environment.

---

## 1. Clone the Repository

```bash
git clone <repository-url>
cd customer-ai-prototype
```

Replace `<repository-url>` with the actual repository URL.

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

The project requires two processes:

```text
Terminal 1 → FastAPI Mock API
Terminal 2 → Streamlit Application
```

---

## Terminal 1 — Start FastAPI

Run:

```bash
python -m uvicorn mock_api:app --reload
```

The API should become available at:

```text
http://127.0.0.1:8000
```

---

## Verify the API

Open:

```text
http://127.0.0.1:8000/customers/101
```

Expected response:

```json
{
    "customer_id": 101,
    "name": "Customer 101",
    "status": "active",
    "segment": "Enterprise",
    "region": "West"
}
```

You can also verify the 404 behavior:

```text
http://127.0.0.1:8000/customers/999
```

---

## Terminal 2 — Start Streamlit

Run:

```bash
python -m streamlit run app.py
```

Streamlit should provide a local URL similar to:

```text
http://localhost:8501
```

Open that URL in your browser.

---

# 🧪 Test Scenarios

The prototype should be tested using multiple scenarios.

## Scenario 1 — Existing Active Customer

Input:

```text
Customer ID: 101
```

Expected:

```text
Customer 101
Status: ACTIVE
```

---

## Scenario 2 — Existing Inactive Customer

Input:

```text
Customer ID: 102
```

Expected:

```text
Customer 102
Status: INACTIVE
```

---

## Scenario 3 — Non-existent Customer

Input:

```text
Customer ID: 999
```

Expected:

```text
Customer 999 was not found.
```

The API should return:

```text
404 Not Found
```

---

## Scenario 4 — Empty Question

Leave the question field empty.

Expected:

```text
Please enter a question.
```

---

## Scenario 5 — API Unavailable

Stop the FastAPI server and attempt to use the application.

Expected:

```text
Unable to connect to the Customer API.
```

The application should fail gracefully rather than crash.

---

## Scenario 6 — API Timeout

If the backend does not respond within the configured timeout:

Expected:

```text
The Customer API request timed out.
```

---

# 🔄 Mock API Strategy

The mock API exists to simulate a backend dependency.

Instead of:

```text
Streamlit
    |
    v
Production Customer API
```

the prototype uses:

```text
Streamlit
    |
    v
Mock Customer API
```

The objective is to preserve the **integration boundary**.

The frontend should communicate through HTTP rather than directly accessing the sample data.

---

# 🧠 Why Not Hardcode the Response?

A simple prototype could do:

```python
answer = "Customer 101 is active."
```

However, that would not demonstrate real API integration.

This project instead follows:

```text
Streamlit
    |
    | HTTP
    v
Mock API
    |
    v
JSON
    |
    v
Streamlit
```

This allows the mock implementation to eventually be replaced by a real API.

---

# 🔁 Prototype → Production

The intended evolution is:

```text
                PROTOTYPE

Streamlit
    |
    v
Mock API
    |
    v
Sample Data
```

↓

```text
                PRODUCTION

Production UI
    |
    v
API Gateway / Backend API
    |
    v
Customer Service
    |
    v
Production Data
    |
    v
AI / LLM Services
```

The prototype should therefore be treated as a **validation layer**, not the final architecture.

---

# 🤖 AI Strategy

The current implementation intentionally uses controlled response logic rather than a real LLM.

For example:

```text
Customer status = active
        |
        v
Generate operational summary
```

There is no need to use an LLM for deterministic operations such as:

* Customer lookup
* Status retrieval
* ID validation

A real LLM becomes more useful when the application needs capabilities such as:

* Natural-language summarization
* Reasoning over multiple data sources
* Unstructured document analysis
* Natural-language question answering
* Contextual explanations

---

# 🔮 Future AI Architecture

A future implementation could look like:

```text
                 User
                  |
                  v
             Application
                  |
                  v
            Customer APIs
                  |
                  v
          Structured Data
                  |
                  +------+
                  |      |
                  v      v
              Retrieval  Business
                  |      Logic
                  +------+
                     |
                     v
                  LLM
                     |
                     v
            Natural Language
                Response
```

If unstructured internal documents are required:

```text
Customer API
     +
Internal Documents
     |
     v
Retrieval / RAG
     |
     v
Relevant Evidence
     |
     v
LLM
     |
     v
Grounded Response
```

RAG should only be introduced where the actual data and retrieval problem justify it.

---

# 🔐 Security Considerations

This is a prototype and is **not production-ready**.

Production implementation would require additional controls such as:

* Authentication
* Authorization
* HTTPS
* Secure secret management
* Input validation
* Rate limiting
* Logging
* Monitoring
* Auditability
* Data protection
* API security

## Secrets

Never store API keys or credentials directly in source code.

Use:

```text
Environment Variables
```

or an appropriate:

```text
Secret Management System
```

The `.gitignore` includes:

```text
.env
.streamlit/secrets.toml
```

to reduce the risk of accidentally committing secrets.

---

# 📊 FDE Perspective

This project demonstrates an FDE-oriented approach to rapid AI prototyping.

The process is:

```text
Customer Problem
       |
       v
User Goal
       |
       v
User Journey
       |
       v
Wireframe
       |
       v
Rapid UI
       |
       v
Mock API
       |
       v
Customer Demonstration
       |
       v
Feedback
       |
       v
Iteration
       |
       v
Productionization
```

The objective is to reduce uncertainty before significant engineering investment.

---

# 💡 Key FDE Principle

> **Prototype the experience, mock the unavailable dependency, preserve the contract, learn from the customer, and only then productionize.**

The purpose of the mock API is therefore not to create a fake production system.

It is to remove a dependency that would otherwise prevent us from validating the user experience.

---

# ⚠️ Prototype Limitations

This project intentionally does not implement:

* Production authentication
* Production authorization
* Real customer database
* Real LLM
* Persistent chat history
* Production monitoring
* Distributed architecture
* Production deployment
* Advanced AI evaluation
* Enterprise observability

These capabilities can be added after the prototype and user workflow have been validated.

---

# 🛣️ Future Roadmap

### Phase 1 — Prototype

* [x] Streamlit UI
* [x] FastAPI mock API
* [x] Customer lookup
* [x] JSON communication
* [x] Error handling
* [x] AI-style response
* [x] Sample data

### Phase 2 — Real Integration

* [ ] Replace mock API
* [ ] Connect real Customer API
* [ ] Externalize API configuration
* [ ] Add authentication
* [ ] Add authorization

### Phase 3 — Real AI

* [ ] Integrate LLM
* [ ] Define AI prompts
* [ ] Add structured output
* [ ] Add AI evaluation
* [ ] Add grounding/citations where required

### Phase 4 — Production

* [ ] Production UI
* [ ] Secure deployment
* [ ] Monitoring
* [ ] Logging
* [ ] Rate limiting
* [ ] Observability
* [ ] CI/CD
* [ ] Security review

---

# 📚 References

* Streamlit Documentation
  [https://docs.streamlit.io/](https://docs.streamlit.io/)

* FastAPI Documentation
  [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

* OpenAPI Specification
  [https://spec.openapis.org/oas/latest.html](https://spec.openapis.org/oas/latest.html)

* Postman Mock Servers
  [https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/)

* WireMock Documentation
  [https://wiremock.org/docs/](https://wiremock.org/docs/)

* Gradio Documentation
  [https://www.gradio.app/docs](https://www.gradio.app/docs)

---

# 🧠 Final Mental Model

```text
Customer Problem
       |
       v
   User Goal
       |
       v
 User Journey
       |
       v
   Wireframe
       |
       v
  Rapid UI
       |
       v
  Mock API
       |
       v
Customer Feedback
       |
       v
    Iterate
       |
       v
  Real API
       |
       v
Production AI Application
```

> **The prototype is successful when it helps us learn whether the solution is worth building—not merely when the code runs.**

````

### One change I'd make before committing

Replace:

```text
git clone <repository-url>
````

## Customer Demo

The Phase 2 customer demonstration is documented in:

[Customer Demo Playbook](/CUSTOMER_DEMO_PLAYBOOK.md)

The demo uses the existing Streamlit application and Mock Customer API
to demonstrate a persona-based customer scenario, success criteria,
synthetic data, failure handling, and customer feedback.
