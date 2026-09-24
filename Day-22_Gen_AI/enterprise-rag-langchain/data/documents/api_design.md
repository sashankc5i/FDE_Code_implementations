# API Design Guidelines

## Overview

APIs should provide predictable interfaces that are easy to consume, test and operate.

## HTTP Methods

Use HTTP methods according to their intended semantics:

- GET for retrieving resources
- POST for creating resources or triggering operations
- PUT for replacing a resource
- PATCH for partial updates
- DELETE for removing resources

## Status Codes

Common response codes include:

- 200 OK for successful requests
- 201 Created when a resource is created
- 400 Bad Request when the request is invalid
- 401 Unauthorized when authentication is required or invalid
- 403 Forbidden when the caller is authenticated but not permitted
- 404 Not Found when the requested resource does not exist
- 500 Internal Server Error for unexpected server-side failures

## Error Responses

Error responses should provide enough information for clients to understand the failure without exposing sensitive implementation details.

## API Versioning

Breaking API changes should use an explicit versioning strategy.

Clients should not unexpectedly break because of an incompatible backend change.

## Observability

Important API operations should produce structured logs containing:

- Request identifier
- Timestamp
- Endpoint
- HTTP method
- Status code
- Processing duration

Sensitive credentials and tokens must not be written to logs.