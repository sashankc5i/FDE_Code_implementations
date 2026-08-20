\# API Data Normalization Pipeline

An asynchronous Python data ingestion and normalization pipeline that consumes external REST API data, preserves the raw JSON response, transforms nested API data into normalized datasets using Pandas, and persists the processed data in CSV and Parquet formats.

The project demonstrates practical Python, HTTP clients, asynchronous programming, data processing, configuration management, testing, and basic production-oriented pipeline design.

\---

\## 1. Project Overview

Modern data applications frequently consume data from external APIs before transforming it into structured datasets for downstream analytics and applications.

This project implements that workflow end-to-end:

\`\`\`text

External REST API

│

▼

Async HTTPX

│

▼

Raw JSON

│

▼

Pandas

│

▼

Normalization

│

┌────┼────────────┐

▼ ▼ ▼

Customers Addresses Companies

│ │ │

└────┼────────────┘

▼

CSV + Parquet

The project uses JSONPlaceholder as the external API source.

**2\. Objectives**

The project was designed to demonstrate practical understanding of:

- JSON processing
- REST API consumption
- HTTP clients
- asynchronous Python
- asyncio
- Pandas
- CSV processing
- Parquet processing
- environment configuration
- Python packaging
- exception handling
- retry logic
- unit testing
- integration testing
- data normalization
- separation of concerns

**3\. Key Features**

**API Ingestion**

Consumes external REST API endpoints using HTTPX.

The pipeline supports:

- synchronous API requests
- asynchronous API requests
- multiple concurrent API requests
- HTTP status validation
- request timeouts

**Asynchronous Processing**

The asynchronous client uses:

httpx.AsyncClient

and:

asyncio.gather()

to execute independent API requests concurrently.

Example:

/users ──────────────┐

/posts ──────────────┼──► asyncio.gather()

/todos ──────────────┘

This is useful for I/O-bound workloads where the application spends significant time waiting for network responses.

**Raw Data Preservation**

The raw API response is preserved before transformation.

API

│

▼

Raw JSON

│

▼

Transformation

This provides a source copy that can be used for:

- debugging
- reprocessing
- auditing
- validating transformation logic

**Data Normalization**

The nested API response contains information about:

- users
- addresses
- geographical coordinates
- companies

The pipeline separates this into logical datasets.

**Customers**

customer_id

name

username

email

phone

website

**Addresses**

customer_id

street

suite

city

zipcode

latitude

longitude

**Companies**

customer_id

company_name

catch_phrase

business_description

**4\. Architecture**

External API

│

▼

AsyncAPIClient

│

┌────────────┼────────────┐

▼ ▼ ▼

/users /posts /todos

│

▼

Raw JSON

│

▼

Normalization Layer

│

┌────────┼─────────┐

▼ ▼ ▼

Customers Addresses Companies

│ │ │

└────────┼─────────┘

▼

Storage Layer

│ │

▼ ▼

CSV Parquet

**5\. Project Structure**

api-data-normalization-pipeline/

│

├── src/

│ └── api_pipeline/

│ ├── \__init_\_.py

│ ├── api_client.py

│ ├── config.py

│ ├── normalization.py

│ ├── pipeline.py

│ └── storage.py

│

├── tests/

│ ├── test_api_client.py

│ ├── test_async_api_client.py

│ ├── test_config.py

│ ├── test_normalization.py

│ ├── test_pipeline.py

│ └── test_storage.py

│

├── data/

│ ├── raw/

│ └── processed/

│

├── .env.example

├── .gitignore

├── main.py

├── pyproject.toml

├── requirements.txt

└── README.md

**6\. Technology Stack**

| **Technology** | **Purpose**               |
| -------------- | ------------------------- |
| Python         | Application development   |
| HTTPX          | HTTP/API communication    |
| AsyncIO        | Asynchronous execution    |
| Pandas         | Data transformation       |
| PyArrow        | Parquet support           |
| python-dotenv  | Environment configuration |
| pytest         | Automated testing         |
| pytest-asyncio | Async test support        |

**7\. Installation**

**Prerequisites**

- Python 3.11+
- pip
- Git

**Clone the repository**

git clone &lt;YOUR_REPOSITORY_URL&gt;

cd api-data-normalization-pipeline

**Create a virtual environment**

Windows:

python -m venv .venv

Activate it:

.venv\\Scripts\\activate

**Install dependencies**

pip install -r requirements.txt

**8\. Environment Configuration**

Create a .env file in the project root.

Example:

API_BASE_URL=<https://jsonplaceholder.typicode.com>

API_TIMEOUT=10

The .env file should not be committed to Git.

A template is provided through:

.env.example

Example:

API_BASE_URL=<https://jsonplaceholder.typicode.com>

API_TIMEOUT=10

**9\. Running the Pipeline**

Run:

python main.py

The pipeline will:

1. Load environment configuration.
2. Initialize the asynchronous HTTP client.
3. Fetch multiple API endpoints concurrently.
4. Preserve the raw /users response.
5. Normalize the nested user data.
6. Create customer, address, and company datasets.
7. Write CSV outputs.
8. Write Parquet outputs.

Example output:

Fetched 10 users.

Fetched 100 posts.

Fetched 200 todos.

Pipeline completed successfully.

Customers: 10

Addresses: 10

Companies: 10

**10\. Output Structure**

After execution:

data/

│

├── raw/

│ └── users.json

│

└── processed/

├── customers.csv

├── customers.parquet

├── addresses.csv

├── addresses.parquet

├── companies.csv

└── companies.parquet

**11\. Testing**

The project uses pytest.

Run the complete test suite:

pytest -v

The current test suite contains:

16 tests

All tests are currently passing.

**Test Categories**

**API Client Tests**

Validate:

- successful HTTP responses
- HTTP error handling

pytest tests/test_api_client.py -v

**Async API Client Tests**

Validate:

- asynchronous API requests
- mocked asynchronous HTTP responses

pytest tests/test_async_api_client.py -v

**Configuration Tests**

Validate:

- API URL configuration
- timeout configuration
- missing configuration
- invalid configuration

pytest tests/test_config.py -v

**Normalization Tests**

Validate:

- customer normalization
- address normalization
- company normalization
- empty API responses

pytest tests/test_normalization.py -v

**Storage Tests**

Validate:

- JSON persistence
- CSV persistence
- Parquet persistence
- unsupported file formats

pytest tests/test_storage.py -v

**Integration Test**

The integration test validates the complete flow:

Mock API

↓

Async HTTP Client

↓

Raw JSON

↓

Pandas Normalization

↓

CSV / Parquet

↓

Read-back validation

Run:

pytest tests/test_pipeline.py -v

The integration test uses httpx.MockTransport, so it does not depend on the availability of the external API.

**12\. Unit Testing vs Integration Testing**

The project intentionally uses both.

**Unit Tests**

Individual components are tested independently:

API Client

Normalization

Configuration

Storage

This makes failures easier to isolate.

**Integration Test**

The integration test verifies that the components work together:

API

↓

Ingestion

↓

Transformation

↓

Persistence

↓

Validation

This provides confidence in the complete data flow.

**13\. Error Handling**

The API client validates unsuccessful HTTP responses using:

response.raise_for_status()

The asynchronous client also handles transient network failures and retries requests using exponential backoff.

Conceptually:

Request

│

├── Success → Continue

│

└── Transient Failure

│

▼

Retry

│

▼

Retry

│

▼

Retry

│

▼

Raise Error

**14\. Why Async Python?**

API ingestion is primarily an I/O-bound workload.

The application spends time waiting for network responses rather than performing CPU-intensive calculations.

Using:

httpx.AsyncClient

with:

asyncio.gather()

allows independent API requests to progress concurrently.

Instead of:

Request 1 → wait → Request 2 → wait → Request 3

the pipeline can perform:

Request 1 ────────┐

Request 2 ────────┼──► responses

Request 3 ────────┘

Async execution is therefore useful when the workload contains many independent I/O operations.

**15\. Why Preserve Raw JSON?**

The raw response is stored before transformation.

This follows a simple principle:

Preserve the source before applying transformations.

Benefits include:

- reproducibility
- debugging
- reprocessing
- auditing
- easier investigation of transformation errors

The architecture therefore separates:

Raw Layer

↓

Transformation Layer

↓

Processed Layer

**16\. Why CSV and Parquet?**

Both formats are supported because they serve different purposes.

**CSV**

Advantages:

- human-readable
- widely supported
- easy to inspect
- useful for simple data exchange

Limitations:

- weak schema preservation
- larger storage footprint
- slower analytical reads for large datasets

**Parquet**

Advantages:

- columnar storage
- efficient analytical reads
- schema-aware
- better compression
- well suited to data engineering workloads

For analytical pipelines, Parquet is generally the preferred processed format.

**17\. Separation of Concerns**

The application separates responsibilities across modules.

api_client.py

↓

HTTP communication

config.py

↓

Environment configuration

normalization.py

↓

Data transformation

storage.py

↓

Data persistence

pipeline.py

↓

Pipeline orchestration

main.py

↓

Application entry point

This makes the code easier to:

- test
- maintain
- extend
- debug

**18\. Design Decisions**

**Raw data is preserved**

The API response is saved before transformation.

**Explicit target schemas**

Instead of relying entirely on automatic JSON flattening, the normalization layer explicitly defines the target fields.

**Dependency injection**

The HTTP client can be supplied to APIClient and AsyncAPIClient.

This allows tests to use:

httpx.MockTransport

without making real network calls.

**Configuration externalization**

API configuration is stored in environment variables rather than hardcoded into application logic.

**Automated testing**

Both component-level and integration-level tests are included.

**19\. Example Normalization**

The API provides nested data such as:

{

"id": 101,

"name": "Arun",

"address": {

"city": "Chennai",

"geo": {

"lat": "13.0827",

"lng": "80.2707"

}

},

"company": {

"name": "ABC Technologies"

}

}

The pipeline transforms this into relational-style datasets.

**Customer**

customer_id | name | email

101 | Arun | <arun@example.com>

**Address**

customer_id | city | latitude | longitude

101 | Chennai | 13.0827 | 80.2707

**Company**

customer_id | company_name

101 | ABC Technologies

The customer_id provides the relationship between the datasets.

**20\. Future Improvements**

Potential extensions include:

- API authentication
- pagination support
- rate-limit handling
- structured logging
- dead-letter/error records
- schema validation using Pydantic
- incremental ingestion
- database persistence
- Dockerization
- CI/CD with GitHub Actions
- orchestration using Airflow or another workflow platform
- data quality checks
- monitoring and metrics

These were intentionally kept outside the initial scope to keep the project focused on API ingestion, normalization, asynchronous processing, and Python engineering fundamentals.

**21\. Learning Outcomes**

This project demonstrates practical application of:

- Python modules and packages
- functions and classes
- exception handling
- type hints
- virtual environments
- environment configuration
- REST APIs
- HTTP clients
- asynchronous programming
- JSON processing
- Pandas transformations
- CSV and Parquet persistence
- unit testing
- integration testing
- dependency injection
- data normalization
- basic production-oriented engineering practices

**22\. Project Status**

**Status: Completed**

The pipeline currently supports:

- asynchronous API ingestion
- concurrent endpoint requests
- raw JSON preservation
- nested JSON normalization
- CSV output
- Parquet output
- environment-based configuration
- retry handling
- unit tests
- integration testing

Current automated test status:

16 tests passed

0 failures

\## One change I'd make before committing

Because you're putting this on GitHub, \*\*don't claim anything that isn't actually in the current code\*\*.

In particular, after adding the retry code, run:

\`\`\`bash

pytest -v

and:

python main.py

If both work, then your README accurately represents the finished project.