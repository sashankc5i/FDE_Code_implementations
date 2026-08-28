# Customer AI Assistant

## Customer Demo & POC Engineering — Demo Playbook

**Phase:** 2 — Customer Demo & POC Engineering
**Demo Duration:** 10 minutes
**Persona:** Operations Manager
**Prototype:** Streamlit Customer AI Assistant
**Backend:** Mock Customer API
**Data:** Synthetic Customer Data

---

# 1. Demo Objective

The objective of this demonstration is to show how an Operations Manager can use a lightweight Customer AI Assistant to retrieve customer information through a simple conversational workflow.

The prototype is intentionally connected to a Mock Customer API rather than a production API.

The purpose of the POC is to validate:

* The customer problem
* The proposed user journey
* The interaction model
* API integration behavior
* Failure handling
* Potential business value
* Customer acceptance and feedback

> **Important:** This prototype demonstrates the proposed experience and integration pattern. It does not claim production readiness.

---

# 2. Customer Problem

The Operations Manager receives requests related to customers and may currently need to manually search systems or depend on an analyst to retrieve and interpret information.

### Current Workflow

```text
Customer Request
       ↓
Manual Search
       OR
Analyst Dependency
       ↓
Wait
       ↓
Review Information
       ↓
Make Decision
```

### Proposed Workflow

```text
Customer Request
       ↓
Customer AI Assistant
       ↓
Customer API
       ↓
Customer Information
       ↓
Operational Decision
```

### Business Hypothesis

The hypothesis is that the Customer AI Assistant can reduce manual effort and dependency on analysts for routine customer-information requests.

This must be validated through customer feedback and measurable success criteria rather than assumed.

---

# 3. Persona

## Operations Manager

### Responsibilities

* Handle operational requests
* Investigate customer situations
* Retrieve information quickly
* Make operational decisions
* Coordinate with analysts and other teams

### Pain Point

The manager may spend significant time manually searching for information or waiting for analyst-generated reports.

### Goal

Retrieve relevant customer information quickly through a simple interaction.

---

# 4. Primary Demo Scenario

### Scenario: Customer Status Investigation

The Operations Manager receives a request regarding **Customer 101**.

The manager needs to determine whether the customer is currently active.

### User Journey

```text
Receive customer request
        ↓
Open Customer AI Assistant
        ↓
Enter Customer ID
        ↓
Ask question
        ↓
Application calls Customer API
        ↓
API returns customer information
        ↓
Assistant presents response
        ↓
Manager makes decision
```

---

# 5. Demo Environment

The prototype consists of:

```text
Streamlit UI
      ↓
HTTP Request
      ↓
Mock Customer API
      ↓
Synthetic Customer Data
      ↓
JSON Response
```

The Mock API is intentionally used because the objective is to demonstrate the workflow without depending on production services.

Before production integration, the actual Customer API contract, authentication, data availability, error behavior, performance and security requirements must be validated.

---

# 6. 10-Minute Demo Script

## 0:00–1:00 — Establish the Problem

### Say

> "Before I show the application, I'd like to start with the operational problem we're trying to solve."
>
> "Let's assume an Operations Manager receives a request regarding a customer and needs to quickly understand the customer's current status."
>
> "Today, depending on the workflow, the manager may need to manually search for that information or depend on an analyst to retrieve and interpret it."
>
> "The question we're exploring is whether we can make that information easier and faster to access."

### Show

No application yet.

Focus entirely on the customer problem.

### Objective

Create relevance before introducing technology.

---

# 7. 1:00–2:00 — Introduce the Persona and Scenario

### Say

> "Let's take the role of the Operations Manager."
>
> "I've just received a request regarding Customer 101 and I need to determine the customer's current status."

Then establish the current process:

> "Under the current workflow, I may need to search for the customer or request information from an analyst."

Then introduce the proposed workflow:

> "With this prototype, the manager can use a single interface to retrieve the information through a natural-language interaction."

### Objective

Make the customer see themselves inside the scenario.

---

# 8. 2:00–3:00 — Introduce the Prototype

Open the Streamlit application.

### Say

> "This is the lightweight prototype we've created to validate the experience."

Explain only the relevant architecture:

```text
Streamlit
    ↓
HTTP Request
    ↓
Mock Customer API
    ↓
JSON Response
```

### Say

> "The API behind this prototype is intentionally mocked. We're using it to simulate the behavior of the future Customer API so that we can validate the user experience and integration pattern before connecting to production."

### Do NOT say

> "This is our production architecture."

Instead:

> **"This demonstrates the proposed interaction and integration pattern."**

---

# 9. 3:00–5:00 — Happy Path: Customer 101

Enter:

```text
Customer ID: 101
```

Ask:

> "What is the current status of this customer?"

### Expected Flow

```text
Streamlit
   ↓
HTTP Request
   ↓
GET /customers/101
   ↓
200 OK
   ↓
JSON Response
   ↓
Customer 101 is active
```

### Say

> "The application sends the request to the Customer API and uses the returned information to provide the response."

Then connect it to the business problem:

> "The important part here isn't simply that the API returned a response. The manager can access the required information through a simpler workflow without manually navigating the underlying API."

---

# 10. 5:00–6:00 — Demonstrate Natural Interaction

Ask a second question supported by the prototype.

Example:

> "Give me the available information for Customer 101."

Explain:

> "This demonstrates that we're moving toward a natural-language interaction rather than requiring the user to understand the underlying API structure."

### Objective

Show the user experience rather than simply demonstrating an API call.

---

# 11. 6:00–7:00 — Intentional Failure Scenario

Now enter:

```text
Customer ID: 999
```

The API should return:

```text
404 Not Found
```

Expected application behavior:

> **Customer 999 was not found.**

### Say

> "I'd like to deliberately demonstrate what happens when the requested customer doesn't exist."

After the response:

> "Notice that the system doesn't assume the customer is inactive. The API has told us that the customer record wasn't found, so we communicate exactly that."

Then:

> "This is important because we don't want the AI to fill missing information with a guess."

### Recovery

> "The user can now correct the Customer ID and continue the workflow."

### Objective

Demonstrate:

* Controlled failure
* Correct API semantics
* No hallucination
* Recovery

---

# 12. 7:00–8:00 — Success Criteria

### Say

> "The POC isn't considered successful simply because the application works technically."

Show the criteria:

| Criterion        | Measurement                           |
| ---------------- | ------------------------------------- |
| Task completion  | User retrieves customer information   |
| Retrieval time   | Compare current workflow vs assistant |
| Accuracy         | Response matches API data             |
| Usability        | User completes the workflow           |
| Failure handling | Errors are controlled                 |
| Adoption         | User is willing to use the workflow   |

### Say

> "These are the hypotheses we'd validate with your team rather than claims we're making from the prototype."

---

# 13. 8:00–9:00 — Production Evolution

### Say

> "The current prototype uses a Mock API because we're validating the experience first."

Show:

```text
CURRENT POC

Streamlit
    ↓
Mock Customer API
    ↓
Synthetic Data
```

Then:

```text
POTENTIAL PRODUCTION

Production UI
      ↓
API / Gateway
      ↓
Customer Services
      ↓
Production Data
      ↓
Authentication
      ↓
Monitoring / Security
```

### Say

> "Before connecting this to the production Customer API, we'd first validate the API contract, authentication mechanism, request and response structure, data availability, error handling, rate limits, performance and security requirements."

### Important

Do not promise a production architecture before understanding the customer's environment.

---

# 14. 9:00–10:00 — Customer Feedback

Do not finish with:

> "Any questions?"

Instead ask:

### Question 1

> **"Where in your current workflow would this remove the most manual effort?"**

### Question 2

> **"What information would you need to see before trusting the response?"**

### Question 3

> **"What would prevent your team from adopting this workflow?"**

If time allows:

> **"If we changed one thing before the next iteration, what would you change?"**

---

# 15. Feedback Handling

Customer feedback should not automatically become a feature request.

Use:

```text
Customer Feedback
       ↓
Understand WHY
       ↓
Underlying Requirement
       ↓
Business Value
       ↓
Technical Feasibility
       ↓
Priority
       ↓
Implementation
```

### Example

Customer:

> "Our managers start with Order ID, not Customer ID."

Response:

> "That's useful context. Let's understand that workflow first and determine how we can adapt the prototype to represent the real process."

Then revisit:

```text
User Journey
      ↓
Wireframe
      ↓
Prototype
      ↓
Success Criteria
```

---

# 16. Demo Success Criteria

The demo should demonstrate:

### Customer Understanding

The customer understands:

* The problem being solved
* Who the solution is for
* How the workflow changes

### Technical Understanding

The customer understands:

* The prototype is functional
* The Mock API represents a replaceable dependency
* API failures are handled
* Production integration requires additional discovery

### Business Understanding

The customer can identify:

* Where the solution could reduce manual effort
* Whether the workflow is valuable
* What information is required
* What could prevent adoption

---

# 17. Demo Failure Plan

If the live prototype fails unexpectedly:

### Primary fallback

Explain the intended workflow using the prepared scenario and architecture.

### Secondary fallback

Use screenshots or recorded outputs of:

```text
Customer 101 → Successful Response
Customer 999 → 404 Response
```

### Never

* Blame the customer environment
* Hide a failure
* Invent an output
* Claim the system worked when it did not

### FDE Principle

> **If the demo breaks, the demo should still continue as a conversation.**

The goal is to validate the POC—not prove that the laptop is invincible.

---

# 18. Demo Do's and Don'ts

## Do

* Start with the customer problem.
* Keep one primary persona.
* Demonstrate one realistic scenario.
* Use controlled synthetic data.
* Demonstrate one intentional failure.
* Explain what the prototype does and does not prove.
* Connect technical behavior to business value.
* Ask targeted feedback questions.
* Capture measurable next steps.

## Don't

* Start with architecture diagrams.
* Show every feature.
* Claim production readiness.
* Use production customer data unnecessarily.
* Hide failures.
* Let AI guess missing information.
* Build every requested feature immediately.
* End with only "Any questions?"

---

# 19. FDE Mental Model

```text
CUSTOMER PROBLEM
       ↓
PERSONA
       ↓
SCENARIO
       ↓
USER JOURNEY
       ↓
PROTOTYPE
       ↓
SUCCESS CRITERIA
       ↓
SYNTHETIC DATA
       ↓
FAILURE HANDLING
       ↓
CUSTOMER DEMO
       ↓
FEEDBACK
       ↓
ITERATION
```

### Core Principle

> **The POC is not the destination. It is the vehicle we use to discover whether the proposed solution is worth taking to production.**

---

# 20. Analogy Mapping

| Analogy                | Phase Concept    | Application                       |
| ---------------------- | ---------------- | --------------------------------- |
| 🚗 Driver              | Persona          | Operations Manager                |
| 🗺️ Route              | User Journey     | Customer investigation            |
| 🎬 Movie Set           | Prototype        | Streamlit + Mock API              |
| 📖 Script              | Scenario         | Customer 101                      |
| 🎞️ Props              | Synthetic Data   | Controlled customer records       |
| 🚪 Fire Exit           | Failure Handling | 404 / API failure                 |
| 🏏 Scorecard           | Success Criteria | Time, accuracy, completion        |
| 🏏 Post-match Analysis | Feedback         | Customer observations             |
| ✍️ Rewrite the Scene   | Iteration        | Update requirements and prototype |

---

# 21. Final FDE Takeaway

A customer demo should not answer only:

> **"What did we build?"**

It should answer:

> **"What customer problem are we solving, how do we know the solution creates value, and what did we learn from demonstrating it?"**

The FDE uses the prototype as a **conversation, validation and learning tool**.

```text
Build
  ↓
Demonstrate
  ↓
Observe
  ↓
Measure
  ↓
Listen
  ↓
Learn
  ↓
Iterate
```

**End of Demo Playbook**
