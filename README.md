# Customer Data Processor

A modular Python data-processing application that generates synthetic customer transaction data, validates data quality, detects duplicates and invalid records, calculates business metrics, and produces a customer data quality report.

The project was designed as a practical demonstration of Python fundamentals applied to a realistic data-processing workflow rather than as a collection of isolated coding exercises.

---

## 1. Overview

The Customer Data Processor simulates a small customer transaction processing system.

The application:

- Generates configurable synthetic customer data
- Introduces duplicate and invalid records for data-quality testing
- Validates incoming customer records
- Handles invalid records without stopping the complete pipeline
- Converts validated records into domain objects
- Calculates customer and transaction metrics
- Produces a consolidated business report
- Supports command-line configuration
- Includes automated unit tests across the application

---

## 2. Business Problem

Customer transaction data frequently contains quality issues such as:

- Duplicate customer IDs
- Missing fields
- Incorrect data types
- Empty transaction histories
- Negative transaction values
- Invalid transaction values

A production data-processing application should not blindly process these records.

Instead, it should:

1. Validate incoming data
2. Separate valid and invalid records
3. Process valid records
4. Capture information about rejected records
5. Produce useful business metrics
6. Provide repeatable and testable behavior

This project simulates that workflow using Python.

---

## 3. Solution Architecture

```text
                    CLI Configuration
                           |
                           v
                  Synthetic Data Generator
                           |
                           v
                     customers.json
                           |
                           v
                       Validation
                           |
                +----------+----------+
                |                     |
                v                     v
          Valid Records        Invalid Records
                |                     |
                v                     v
        Customer Objects       Error Capture
                |
                v
            Processing
                |
                v
             Reporting
                |
                v
           Final Report


### Application Layers

The application is divided into separate responsibilities:

| Layer                      | Responsibility                                         |
| -------------------------- | ------------------------------------------------------ |
| `scripts/generate_data.py` | Generate configurable synthetic customer data          |
| `models.py`                | Represent customer data and customer-specific behavior |
| `validation.py`            | Validate incoming customer records                     |
| `exceptions.py`            | Define application-specific exceptions                 |
| `processing.py`            | Perform business calculations                          |
| `reporting.py`             | Combine processing results into a business summary     |
| `service.py`               | Orchestrate validation, processing, and reporting      |
| `main.py`                  | Application entry point, CLI handling, and output      |

This separation allows individual components to be tested and modified independently.

---

## 5. Key Capabilities

### Synthetic Data Generation

The application can generate configurable customer datasets with:

* Configurable number of customers
* Configurable duplicate rate
* Configurable invalid-record rate
* Random customer names
* Random countries
* Random transaction histories
* Reproducible data generation using a deterministic random seed

Example:

```bash
python scripts/generate_data.py \
    --customers 1000 \
    --duplicates 0.05 \
    --invalid 0.02
```

The generated records are stored in:

```text
data/customers.json
```

### Data Validation

Incoming records are validated before processing.

Validation checks include:

* Required fields
* Customer ID type
* Customer name type
* Country type
* Transaction list type
* Non-empty transaction history
* Numeric transaction values
* Non-negative transaction values

Invalid records raise the custom:

```python
InvalidCustomerDataError
```

### Customer Domain Model

Validated records are converted into `Customer` objects.

The `Customer` model provides behavior for:

```python
customer.total_spend()
customer.average_transaction()
customer.is_high_value(threshold)
```

This keeps customer-specific business behavior close to the customer data it operates on.

### Business Processing

The application calculates:

* High-value customers
* Unique countries
* Duplicate customer IDs
* Average transaction value
* Highest transaction value
* Total valid customer records
* Invalid customer record count

### Graceful Error Handling

Invalid records do not automatically terminate the complete processing pipeline.

Instead:

```text
Valid Record
    ↓
Processed

Invalid Record
    ↓
Validation Exception
    ↓
Captured
    ↓
Reported
```

This allows valid records to continue through the pipeline while maintaining visibility into data-quality issues.

### Command-Line Configuration

The application supports runtime configuration without requiring source-code changes.

Generate data:

```bash
python scripts/generate_data.py --customers 1000 --duplicates 0.10 --invalid 0.02
```

Run the processor with a custom threshold:

```bash
python main.py --threshold 5000
```

---

## 6. Project Structure

```text
customer-data-processor/
│
├── customer_app/
│   ├── __init__.py
│   ├── models.py
│   ├── exceptions.py
│   ├── validation.py
│   ├── processing.py
│   ├── reporting.py
│   └── service.py
│
├── scripts/
│   ├── __init__.py
│   └── generate_data.py
│
├── data/
│   └── customers.json
│
├── tests/
│   ├── __init__.py
│   ├── test_generate_data.py
│   ├── test_models.py
│   ├── test_validation.py
│   ├── test_processing.py
│   ├── test_reporting.py
│   ├── test_service.py
│   ├── test_cli.py
│   └── test_main.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Module Responsibilities

#### `customer_app/models.py`

Contains the `Customer` domain model and customer-specific behavior.

#### `customer_app/exceptions.py`

Contains custom application exceptions such as:

```python
InvalidCustomerDataError
```

#### `customer_app/validation.py`

Validates raw customer dictionaries before they are converted into domain objects.

#### `customer_app/processing.py`

Contains reusable business-processing functions such as:

```python
get_high_value_customers()
get_unique_countries()
find_duplicate_customer_ids()
calculate_average_transaction()
get_highest_transaction()
```

#### `customer_app/reporting.py`

Combines calculated metrics into a structured summary.

#### `customer_app/service.py`

Provides the application-level processing workflow:

```text
Raw Data
   ↓
Validation
   ↓
Valid / Invalid Separation
   ↓
Customer Creation
   ↓
Business Processing
   ↓
Summary
```

#### `scripts/generate_data.py`

Generates synthetic customer data and writes it to JSON.

#### `main.py`

Acts as the application entry point.

It handles:

* Command-line arguments
* Loading the JSON dataset
* Calling the application service
* Printing the final report

---

## 7. Python Concepts Demonstrated

This project demonstrates Python concepts through a working application rather than isolated examples.

### Data Structures

The project uses:

* Lists
* Dictionaries
* Sets
* Nested data structures
* List comprehensions
* Set comprehensions
* Generator expressions
* `Counter`

Example:

```python
unique_countries = {
    customer.country
    for customer in customers
}
```

### Functions

Functions are used as reusable units of business logic.

The project demonstrates:

* Function parameters
* Default arguments
* Return values
* Keyword arguments
* Type annotations
* Function composition
* Reusable helper functions

Example:

```python
def get_high_value_customers(
    customers: list[Customer],
    threshold: float,
) -> list[Customer]:
    ...
```

### Classes and Objects

The `Customer` class encapsulates both customer data and customer-specific behavior.

```python
customer = Customer(
    customer_id=101,
    name="Arun",
    country="India",
    transactions=[1200, 500, 800],
)
```

Behavior is exposed through methods:

```python
customer.total_spend()
customer.average_transaction()
customer.is_high_value(2000)
```

### Modules

The application is split into modules based on responsibility:

```text
models
exceptions
validation
processing
reporting
service
```

This prevents unrelated responsibilities from being concentrated in a single file.

### Packages

The `customer_app` and `scripts` directories are structured as Python packages using `__init__.py`.

### Exception Handling

The project demonstrates:

* Custom exceptions
* `raise`
* `try`
* `except`
* Exception messages
* Graceful handling of invalid records

Example:

```python
try:
    validate_customer_data(customer_data)

except InvalidCustomerDataError as error:
    invalid_customer_data.append(
        {
            "data": customer_data,
            "error": str(error),
        }
    )
```

### Type Hints

Type hints are used throughout the application to make interfaces explicit.

Examples:

```python
list[dict]
list[Customer]
set[str]
float
bool
None
```

### JSON and File Handling

The project uses Python's standard library to:

* Read JSON files
* Write JSON files
* Work with filesystem paths
* Persist generated datasets

### Command-Line Interfaces

Python's `argparse` module is used to make the application configurable from the command line.

Example:

```bash
python main.py --threshold 5000
```

### Automated Testing

`pytest` is used to test individual modules and application behavior.

The test suite covers:

* Normal cases
* Edge cases
* Invalid inputs
* Exception behavior
* Data generation
* Business logic
* Reporting
* Service orchestration
* CLI arguments
* Application entry points

---

## 8. Setup

### Prerequisites

Make sure the following are installed:

* Python 3.10+
* `pip`
* Git

Verify the Python installation:

```bash
python --version
```

Verify `pip`:

```bash
pip --version
```

### Clone the Repository

```bash
git clone <repository-url>
cd customer-data-processor
```

### Create a Virtual Environment

Creating a virtual environment isolates the project's dependencies from the system Python installation.

#### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, the terminal should indicate that the virtual environment is active.

### Install Dependencies

Install the project's dependencies:

```bash
pip install -r requirements.txt
```

The primary development dependency is:

```text
pytest
```

### Verify the Installation

Run the test suite:

```bash
pytest -v
```

A successful setup should result in all tests passing.

---

## 9. Synthetic Data Generation

The project does not rely on manually hardcoded customer records. Instead, it generates configurable synthetic data for development and testing.

The generator can simulate:

* Normal customer records
* Duplicate customer IDs
* Invalid customer records
* Different countries
* Different transaction counts
* Different transaction values

### Generate Default Dataset

Run:

```bash
python scripts/generate_data.py
```

The generated dataset is stored at:

```text
data/customers.json
```

### Generate a Custom Dataset

The generator supports three configurable parameters:

| Argument       | Description                  | Example |
| -------------- | ---------------------------- | ------- |
| `--customers`  | Number of original customers | `1000`  |
| `--duplicates` | Duplicate-record rate        | `0.05`  |
| `--invalid`    | Invalid-record rate          | `0.02`  |

Example:

```bash
python scripts/generate_data.py --customers 1000 --duplicates 0.05 --invalid 0.02
```

This generates approximately:

```text
1000 original records
+ 50 duplicate records
+ 20 invalid records
= 1070 records
```

### View Available Options

```bash
python scripts/generate_data.py --help
```

### Reproducible Data Generation

The generator uses a deterministic random seed during normal execution.

This allows the same configuration to produce the same dataset, which is useful for:

* Testing
* Debugging
* Reproducing issues
* Demonstrating the application consistently

---

## 10. Running the Application

The application processes the generated JSON dataset and produces a customer data-quality report.

### Step 1 — Generate Data

```bash
python scripts/generate_data.py
```

Or generate a custom dataset:

```bash
python scripts/generate_data.py \
    --customers 100 \
    --duplicates 0.05 \
    --invalid 0.05
```

### Step 2 — Run the Application

Run with the default high-value threshold:

```bash
python main.py
```

The application will:

1. Load `data/customers.json`
2. Validate customer records
3. Separate valid and invalid records
4. Convert valid records into `Customer` objects
5. Calculate business metrics
6. Generate the final summary
7. Print the report

### Configure the High-Value Threshold

The high-value threshold can be changed without modifying the source code.

For example:

```bash
python main.py --threshold 2000
```

or:

```bash
python main.py --threshold 5000
```

This changes which customers are classified as high-value.

### View Application Options

```bash
python main.py --help
```

### Example Workflow

A complete execution can be performed with:

```bash
python scripts/generate_data.py --customers 100 --duplicates 0.05 --invalid 0.05
```

followed by:

```bash
python main.py --threshold 2000
```

The resulting report will contain metrics based on the generated dataset.

---

## 11. Data Validation & Error Handling

Data validation is performed before customer records enter the business-processing layer.

The validation pipeline is:

```text
Raw Customer Record
        |
        v
Required Field Validation
        |
        v
Type Validation
        |
        v
Transaction Validation
        |
        +----------------------+
        |                      |
      Valid                  Invalid
        |                      |
        v                      v
Customer Object       InvalidCustomerDataError
        |                      |
        v                      v
Business Processing     Error Captured
        |                      |
        +----------+-----------+
                   |
                   v
                 Report
```

### Validation Rules

Each customer record must contain:

```text
id
name
country
transactions
```

The following rules are enforced:

#### Customer ID

The customer ID must be an integer.

Valid:

```json
{
    "id": 101
}
```

Invalid:

```json
{
    "id": "101"
}
```

#### Customer Name

The customer name must be a string.

#### Country

The country must be represented as a string.

#### Transactions

Transactions must:

* Be represented as a list
* Contain at least one value
* Contain numeric values
* Not contain negative values

Valid:

```json
{
    "transactions": [1200, 500, 800]
}
```

Invalid:

```json
{
    "transactions": []
}
```

Invalid:

```json
{
    "transactions": [1200, -500]
}
```

Invalid:

```json
{
    "transactions": [1200, "INVALID"]
}
```

### Custom Exception

Invalid records raise:

```python
InvalidCustomerDataError
```

defined in:

```text
customer_app/exceptions.py
```

This allows the application to distinguish expected customer-data validation failures from unrelated system errors.

### Graceful Error Handling

The service layer catches validation errors individually:

```python
try:
    validate_customer_data(customer_data)

except InvalidCustomerDataError as error:
    invalid_customer_data.append(
        {
            "data": customer_data,
            "error": str(error),
        }
    )
```

Therefore, an invalid record does not automatically terminate processing of all other records.

For example:

```text
Customer 101  → Valid   → Processed
Customer 102  → Valid   → Processed
Customer 103  → Invalid → Captured
Customer 104  → Valid   → Processed
Customer 105  → Valid   → Processed
```

This approach allows the application to continue processing usable data while retaining visibility into data-quality issues.

### Why This Design?

The validation layer is intentionally separated from the processing layer.

This allows the application to evolve from:

```text
JSON → Validation → Processing
```

to potentially:

```text
API → Validation → Processing
```

or:

```text
Database → Validation → Processing
```

without requiring the core business-processing logic to be rewritten.
## 12. Testing

The project uses `pytest` for automated testing.

Run the complete test suite:

```bash
pytest -v

**Important:** replace `37` with the actual number you get from your final `pytest -v`.

---

### 13. Design Decisions

This is particularly valuable for your FDE goal:

```markdown
## 13. Design Decisions

### Separation of Concerns

The application separates validation, business processing, reporting, and orchestration into independent modules.

This makes individual components easier to test, debug, and modify.

### Domain Model

Customer-specific behavior is encapsulated in the `Customer` class instead of repeatedly manipulating raw dictionaries.

### Graceful Data-Quality Handling

Invalid records are captured and reported rather than terminating the entire processing workflow.

### Configurable Execution

Dataset size, duplicate rate, invalid rate, and high-value thresholds can be changed through CLI arguments without modifying source code.

### Service Layer

The service layer separates the application workflow from the data source and command-line interface.

This allows the same business logic to potentially process data received from JSON, APIs, databases, or other sources.

### Testability

Business logic is implemented through small, reusable functions and tested independently before being composed into the complete application.

## 14. Future Improvements

Potential extensions include:

- REST API ingestion
- Database integration
- CSV ingestion
- Structured logging
- Invalid-record quarantine
- Configuration through environment variables
- Docker containerization
- GitHub Actions CI/CD
- Data-quality monitoring
- Retry mechanisms
- Idempotent processing
- Cloud storage integration
- Spark-based large-scale processing
- Observability and operational metrics