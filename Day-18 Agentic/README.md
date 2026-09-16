# AI Data Engineering Incident Response Agent

> **FDE Training Project — Agentic AI**

An agentic AI system that investigates data engineering pipeline incidents, gathers evidence from multiple systems, classifies the likely failure type, recommends controlled remediation, enforces safety policies, and validates recovery.

The project is intentionally implemented as a **training/POC system using simulated data engineering infrastructure**. Its purpose is to demonstrate the engineering patterns required to design reliable enterprise AI agents rather than reproduce a complete production incident-management platform.

---

## 1. Problem Statement

When a production data pipeline fails, engineers typically need to investigate several systems before determining what happened:

* Pipeline execution status
* Execution logs
* Source table schemas
* Deployment history
* Infrastructure information
* Previous remediation attempts

A simple LLM chatbot cannot safely perform this workflow because it needs to:

1. Determine what information is missing.
2. Select appropriate tools.
3. Investigate multiple systems.
4. Interpret evidence.
5. Decide whether more investigation is required.
6. Classify the failure.
7. Determine whether remediation is appropriate.
8. Respect authorization and safety policies.
9. Request human approval for risky actions.
10. Validate the result.

This project implements that workflow as an **agentic incident-response system**.

---

# 2. Example Incident

A user reports:

> "Why did the Customer 360 pipeline fail?"

The agent investigates:

```text
Customer 360
      ↓
Find canonical pipeline ID
      ↓
Get pipeline status
      ↓
Get execution logs
      ↓
Identify affected source table
      ↓
Inspect table schema
      ↓
Compare failure evidence with schema
      ↓
Classify failure
```

The simulated incident produces:

```text
Pipeline:
Customer 360

Status:
FAILED

Failure:
AnalysisException:
Cannot resolve column 'customer_segment'

Source schema:
customer_id
customer_name
email
country
segment
created_date
```

The agent identifies the likely issue:

```text
Transformation expects:
customer_segment

Source actually contains:
segment
```

The system therefore classifies the incident as:

```text
SCHEMA_DRIFT
```

Importantly, the agent distinguishes between:

* **Observed evidence**
* **Likely root cause**
* **Unresolved underlying cause**

It does not invent evidence that is unavailable.

---

# 3. Why an Agent?

This problem is not simply:

```text
User → LLM → Answer
```

The system must dynamically decide what to investigate next.

The agent follows:

```text
Goal
 ↓
Plan
 ↓
Reason
 ↓
Act
 ↓
Observe
 ↓
Update state
 ↓
Re-plan
 ↓
Finish
```

For example:

```text
User:
"Why did Customer 360 fail?"

        ↓

Agent:
"I need the canonical pipeline ID."

        ↓

find_pipeline()

        ↓

Agent:
"I know the pipeline ID.
I need the failure information."

        ↓

get_pipeline_status()

        ↓

Agent:
"The failure is related to an unresolved column.
I need execution evidence."

        ↓

get_pipeline_logs()

        ↓

Agent:
"The logs identify customer_master.
I should inspect its schema."

        ↓

get_table_schema()

        ↓

Agent:
"Sufficient evidence exists."

        ↓

CLASSIFY_FAILURE

        ↓

Answer
```

This dynamic investigation loop is the core agentic behavior.

---

# 4. Architecture

## Logical Architecture

```text
                           USER
                            │
                            ▼
                   ┌─────────────────┐
                   │ Incident Agent  │
                   │ / Orchestrator  │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   Supervisor    │
                   │   LLM Decision  │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
         Log Agent      Data Agent   Deployment Agent
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                   ┌─────────────────┐
                   │ Evidence / State│
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │Failure Classifier│
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │ Remediation Plan│
                   └────────┬────────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
             Safe Operation    Human Approval
                    │                │
                    └───────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │  Policy Gate    │
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │   Remediation   │
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │   Validation    │
                   └────────┬────────┘
                            ▼
                     SUCCESS / FAILED
```

---

# 5. Agent Responsibilities

## Incident Agent

The main investigation agent.

Responsibilities:

* Understand the incident request.
* Decide which tools are needed.
* Maintain investigation context.
* Gather evidence.
* Avoid repeated tool calls.
* Stop once sufficient evidence exists.
* Escalate when evidence is insufficient.

---

## Supervisor

The supervisor determines which specialist investigations are relevant.

Available specialists:

```text
log
data
deployment
```

For example:

```text
Missing column
      ↓
log + data
```

Whereas:

```text
Deployment failure
      ↓
log + deployment
```

This allows investigations to run independently and, where appropriate, in parallel.

---

## Log Agent

Investigates pipeline execution logs.

Responsibilities:

* Retrieve pipeline logs.
* Extract error-level events.
* Return structured findings.
* Report tool/system failure independently.

---

## Data Agent

Investigates source data/schema evidence.

Responsibilities:

* Inspect source table schemas.
* Identify relevant columns.
* Provide schema evidence.
* Report failures without affecting other specialists.

---

## Deployment Agent

Represents deployment investigation capability.

The training implementation currently provides a controlled placeholder for this capability.

A production implementation would integrate with deployment systems such as CI/CD platforms.

---

## Remediation Agent

Determines whether an action can safely be attempted.

Examples:

```text
SCHEMA_DRIFT
    ↓
No automatic remediation
    ↓
Human investigation

INFRASTRUCTURE
    ↓
Restart may be possible
    ↓
Human approval
```

The system deliberately does **not** assume that every failure can be fixed automatically.

---

## Validation Agent

Verifies whether recovery actually occurred.

The principle is:

```text
Action ≠ Recovery
```

A remediation action is not considered successful until the resulting system state has been validated.

---

# 6. Tool Calling

The agent uses explicit tools rather than unrestricted system access.

Current tools include:

```text
find_pipeline
get_pipeline_status
get_pipeline_logs
get_table_schema
```

Remediation/validation tools include:

```text
restart_pipeline
validate_pipeline
```

The LLM only proposes tool calls.

The application executes them.

```text
LLM
 ↓
Tool proposal
 ↓
Application validation
 ↓
Tool execution
 ↓
Observation
 ↓
Agent reasoning
```

The LLM is therefore **not the authorization layer**.

---

# 7. Canonical Identifier Resolution

A common agent failure is assuming internal identifiers.

For example, the user may say:

```text
Customer 360
```

while the system requires:

```text
customer_360
```

The agent therefore performs:

```text
Human-readable name
        ↓
find_pipeline()
        ↓
Canonical pipeline ID
        ↓
customer_360
```

Once the canonical ID has been obtained, the agent reuses it instead of repeatedly searching.

This demonstrates an important tool-use pattern:

> Resolve human context into canonical system identifiers before performing downstream operations.

---

# 8. Persistent State

Incident state is represented using Pydantic models.

Example:

```text
IncidentState
├── incident_id
├── pipeline_id
├── current_state
├── failure_type
├── observations
├── actions_taken
├── llm_iterations
├── tool_calls
├── confidence
├── requires_human
├── approval_required
├── approval_status
├── pending_action
└── last_error
```

State is persisted through a checkpoint store.

The training implementation uses JSON checkpoints.

A production system would typically use a durable transactional store.

---

# 9. State Machine

The incident lifecycle is explicitly controlled by a state machine.

```text
START
  ↓
INVESTIGATING
  ↓
CLASSIFYING
  ↓
REMEDIATING
  ↓
VALIDATING
  ↓
SUCCESS
```

Alternative paths include:

```text
INVESTIGATING
      ↓
   ESCALATED
```

and:

```text
CLASSIFYING
      ↓
APPROVAL_PENDING
      ↓
REMEDIATING
```

Terminal states:

```text
SUCCESS
FAILED
ESCALATED
```

Invalid transitions are rejected by the application.

This prevents the LLM from arbitrarily changing workflow state.

---

# 10. Parallel Specialist Investigation

Independent investigations can run concurrently.

```text
                 Supervisor
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Log Agent  Data Agent  Deploy Agent
          │          │          │
          └──────────┼──────────┘
                     ▼
                  Evidence
```

The implementation uses Python concurrency with:

```python
ThreadPoolExecutor
```

This demonstrates an important distributed-agent pattern:

> Independent evidence collection should not necessarily be performed sequentially.

---

# 11. Failure Isolation

A specialist failure should not automatically terminate the entire investigation.

Example:

```text
Log Agent
    ↓
FAILED

Data Agent
    ↓
COMPLETED

Supervisor
    ↓
Continue with available evidence
```

The system captures specialist failures independently.

This was explicitly tested in the project.

---

# 12. Safety and Policy

Agentic systems become significantly more sensitive once they can modify external systems.

The project therefore defines risk levels:

```text
READ
LOW_RISK_WRITE
HIGH_RISK_WRITE
DESTRUCTIVE
```

Example policy:

| Operation             | Risk            | Behavior          |
| --------------------- | --------------- | ----------------- |
| `get_pipeline_status` | READ            | Allowed           |
| `get_pipeline_logs`   | READ            | Allowed           |
| `get_table_schema`    | READ            | Allowed           |
| `create_incident`     | LOW_RISK_WRITE  | Allowed           |
| `restart_pipeline`    | HIGH_RISK_WRITE | Approval required |
| `rollback_deployment` | HIGH_RISK_WRITE | Approval required |
| `disable_pipeline`    | DESTRUCTIVE     | Explicit approval |
| Unknown tool          | UNKNOWN         | Blocked           |

The security boundary is:

```text
LLM proposes
     ↓
Policy Gate
     ↓
Authorization decision
     ↓
Execution
```

Not:

```text
LLM proposes
     ↓
Execute immediately
```

---

# 13. Human-in-the-Loop

High-risk actions require human approval.

Example:

```text
Infrastructure failure
        ↓
Restart pipeline recommended
        ↓
APPROVAL_PENDING
        ↓
Human decision
        │
    ┌───┴───┐
    ▼       ▼
 APPROVE   REJECT
    │       │
    ▼       ▼
REMEDIATING ESCALATED
```

This establishes an explicit human decision boundary.

---

# 14. Remediation

The training environment contains a simulated remediation system.

Example:

```text
restart_pipeline()
```

can transition a simulated pipeline from:

```text
FAILED
```

to:

```text
RUNNING
```

Validation then checks the resulting state.

However, the system intentionally does **not** pretend that restarting fixes every incident.

For example:

```text
SCHEMA_DRIFT
```

requires transformation/schema correction and therefore remains a human investigation case.

This demonstrates:

> Automated remediation must be based on failure semantics, not simply on the existence of an available tool.

---

# 15. Failure Classification

The classifier currently recognizes:

```text
SCHEMA_DRIFT
DATA_QUALITY
INFRASTRUCTURE
DEPLOYMENT
UNKNOWN
```

The classification uses observed evidence.

For example:

```text
AnalysisException
+
Cannot resolve column
+
Current schema evidence
        ↓
SCHEMA_DRIFT
```

The classifier deliberately avoids overly broad keyword rules that could incorrectly classify unrelated failures.

---

# 16. Evaluation

The project includes an evaluation layer that captures:

```text
incident_id
failure_type
llm_iterations
tool_calls
successful_tool_calls
failed_tool_calls
specialist_agents
specialist_failures
human_escalation
remediation_attempted
remediation_success
validation_attempted
validation_success
diagnosis_correct
investigation_success
```

The purpose is to evaluate the **agent system**, not simply whether the LLM generated a plausible answer.

Important evaluation dimensions include:

### Diagnosis Accuracy

Did the agent classify the incident correctly?

### Tool Reliability

Did tools execute successfully?

### Investigation Efficiency

How many iterations and tool calls were required?

### Failure Isolation

Did one failed specialist prevent the remaining investigation?

### Safety Compliance

Were risky operations correctly gated?

### Recovery Validation

Was successful recovery actually verified?

---

# 17. Test Results

The current training implementation has a passing test suite covering:

```text
✓ Smoke test
✓ Supervisor decision
✓ Parallel specialist investigation
✓ Specialist failure isolation
✓ Read-only policy enforcement
✓ High-risk approval enforcement
✓ Destructive-action blocking
✓ Unknown-tool blocking
✓ Incident evaluation
```

Current result:

```text
10 passed
```

The tests demonstrate that the core agentic architecture is functioning as intended in the simulated environment.

---

# 18. Project Structure

```text
agentic-incident-response/
│
├── app/
│   ├── agents/
│   │   ├── incident_agent.py
│   │   ├── supervisor.py
│   │   ├── log_agent.py
│   │   ├── data_agent.py
│   │   ├── deployment_agent.py
│   │   ├── remediation_agent.py
│   │   ├── validation_agent.py
│   │   └── failure_classifier.py
│   │
│   ├── tools/
│   │   └── pipeline_tools.py
│   │
│   ├── workflows/
│   │   ├── state_machine.py
│   │   ├── state_manager.py
│   │   └── checkpoint_store.py
│   │
│   ├── safety/
│   │   ├── policies.py
│   │   └── policy_gate.py
│   │
│   ├── evaluation/
│   │   └── evaluator.py
│   │
│   ├── models/
│   │   ├── incident_state.py
│   │   └── evaluation.py
│   │
│   └── llm/
│       └── groq_client.py
│
├── simulation/
│   ├── pipeline_system.py
│   ├── remediation_system.py
│   └── incident_ground_truth.py
│
├── tests/
│
├── checkpoints/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml
```

---

# 19. Technology Stack

## AI / Agent

* Python
* Groq API
* `openai/gpt-oss-20b`
* Function/tool calling
* Structured JSON outputs

## Application

* Python
* Pydantic
* Pydantic Settings

## Agent Architecture

* Supervisor + specialist agents
* Tool calling
* Persistent state
* Explicit state machine
* Parallel investigation
* Human-in-the-loop
* Policy enforcement

## Testing

* pytest
* httpx

## Training Infrastructure

The project uses simulated pipeline infrastructure rather than real production systems.

---

# 20. Production Azure Architecture

The training project intentionally separates the **learning implementation** from the production target architecture.

A production deployment could map the components as follows:

| Capability           | Azure Technology                          |
| -------------------- | ----------------------------------------- |
| Application runtime  | Azure Container Apps                      |
| Transactional state  | Azure SQL Database                        |
| Documents/content    | Azure Blob Storage                        |
| RAG/search           | Azure AI Search                           |
| AI platform          | Azure AI Foundry                          |
| Background workloads | Container Apps Jobs / Azure Functions     |
| Identity             | Microsoft Entra ID                        |
| Secrets              | Azure Key Vault                           |
| Network isolation    | Azure VNet + Private Endpoints            |
| Monitoring           | Azure Monitor + Application Insights      |
| AI evaluation        | Azure AI Foundry evaluation/observability |
| Security posture     | Microsoft Defender for Cloud              |
| Governance           | Azure Policy                              |
| CI/CD                | Azure DevOps                              |
| Backup/DR            | Azure-native backup + enterprise strategy |

The production security boundary would remain:

```text
User
 ↓
API
 ↓
Agent Orchestrator
 ↓
LLM
 ↓
Tool proposal
 ↓
Authorization / Policy
 ↓
Approved internal API
 ↓
Production system
```

---

# 21. Training POC vs Production System

This repository is intentionally **not** a full production implementation.

### Training POC

```text
Groq
 ↓
Python Agent
 ↓
Simulated pipeline systems
 ↓
JSON checkpoint
 ↓
Local tests
```

### Production Architecture

```text
Azure Container Apps
        ↓
Azure AI Foundry
        ↓
Enterprise tools/APIs
        ↓
Azure SQL
        ↓
Entra ID / Key Vault
        ↓
VNet / Private Endpoints
        ↓
Azure Monitor / App Insights
```

The POC proves the **agentic design patterns**.

The production architecture describes how those patterns could be implemented within an enterprise Azure environment.

---

# 22. Key FDE Engineering Lessons

This project demonstrates several important FDE principles.

### 1. LLMs are decision-support components

The LLM should not directly control authorization or production infrastructure.

---

### 2. Tools are contracts

A tool defines what the agent can request.

The application still owns:

* Validation
* Authorization
* Business rules
* Risk controls
* Execution

---

### 3. Evidence before conclusions

The agent should investigate before declaring a root cause.

```text
Symptom
 ↓
Evidence
 ↓
Hypothesis
 ↓
Additional evidence
 ↓
Diagnosis
```

---

### 4. Failure is part of the workflow

Tool failures and specialist failures are expected system states.

They should be captured and handled rather than hidden.

---

### 5. State is different from conversation history

Operational state represents what the system currently knows and is doing.

Conversation history is contextual information.

They should not be treated as the same thing.

---

### 6. Automation must have boundaries

Not every problem should be automatically fixed.

Some failures should result in:

```text
ESCALATED
```

rather than unsafe automation.

---

### 7. Validation matters

Executing an action does not prove recovery.

Always verify the resulting system state.

---

### 8. Evaluation must measure the system

A successful LLM response is not sufficient.

Agentic systems should be evaluated across:

```text
Reasoning
Tool use
Reliability
Safety
Recovery
Escalation
Efficiency
```

---

# 23. Known Limitations

This repository is a training POC.

It intentionally does not implement the complete production infrastructure required for a real enterprise incident platform.

Current limitations include:

* Simulated pipeline infrastructure
* Simulated remediation
* Local JSON checkpoint persistence
* Limited deployment investigation
* No real production pipeline APIs
* No enterprise identity integration
* No production network isolation
* No distributed action store
* No full production observability backend
* No production-scale concurrency testing

These are deliberate scope boundaries rather than missing requirements for the training objective.

---

# 24. Running the Project

## 1. Clone the repository

```bash
git clone <repository-url>
cd agentic-incident-response
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Copy:

```text
.env.example
```

to:

```text
.env
```

Set:

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

## 5. Run the tests

```bash
pytest -v
```

Expected result:

```text
10 passed
```

---

# 25. Example Investigation

Input:

```text
Why did the Customer 360 pipeline fail?
```

Agent investigation:

```text
find_pipeline
      ↓
get_pipeline_status
      ↓
get_pipeline_logs
      ↓
get_table_schema
      ↓
failure classification
```

Result:

```text
Failure Type:
SCHEMA_DRIFT

Likely Root Cause:
The transformation references customer_segment,
while the current customer_master schema contains segment.

Evidence:
- Pipeline failure reports unresolved customer_segment.
- Logs identify customer_master.
- Current schema contains segment.
- Current schema does not contain customer_segment.
```

---

# 26. Project Outcome

This project demonstrates an end-to-end agentic AI architecture for data engineering incident response.

The key outcome is not simply:

> "An LLM can call tools."

The project demonstrates how to build a controlled system around the LLM:

```text
LLM
 ↓
Planning
 ↓
Tool selection
 ↓
Evidence collection
 ↓
Parallel investigation
 ↓
State management
 ↓
Failure classification
 ↓
Policy enforcement
 ↓
Human approval
 ↓
Remediation
 ↓
Validation
 ↓
Evaluation
```

That is the central engineering lesson of the project.

---

## Final Architecture Principle

> **The LLM provides reasoning and decision support; the application owns state, authorization, execution, safety, and validation.**

This separation is the foundation for building reliable enterprise agentic AI systems.
