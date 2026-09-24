# Azure Container Apps Operations Guide

## Overview

Azure Container Apps provides a managed environment for running containerized applications.

Applications commonly consist of a frontend service and a backend API service.

## Environment Configuration

Application configuration can include:

- Environment variables
- Managed identity configuration
- Ingress configuration
- Container image configuration
- Secret references
- Domain configuration

Sensitive values should not be stored directly in application source code.

## Custom Domains

When a custom domain is introduced, validate:

1. DNS configuration
2. Domain binding
3. TLS configuration
4. Application redirect URI configuration
5. Authentication token audience configuration
6. Frontend and backend endpoint configuration

A domain change can require corresponding updates to authentication configuration.

## Application Troubleshooting

When an application becomes unavailable after a deployment or configuration change:

1. Verify the container revision is running.
2. Check application logs.
3. Verify ingress configuration.
4. Verify environment variables.
5. Verify secrets and secret references.
6. Test the backend endpoint independently.
7. Test the frontend-to-backend connection.
8. Review authentication configuration when requests return HTTP 401.

## Deployment Verification

After deploying a new revision:

- Confirm the revision becomes healthy.
- Verify the expected container image is running.
- Test the primary application endpoint.
- Test critical API endpoints.
- Review application logs.
- Validate authentication.