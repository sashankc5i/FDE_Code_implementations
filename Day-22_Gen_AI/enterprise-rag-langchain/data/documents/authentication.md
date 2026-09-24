# Authentication Troubleshooting Guide

## Overview

Authentication failures occur when an application cannot successfully validate the identity or authorization information associated with a request.

A common HTTP response associated with authentication failure is HTTP 401 Unauthorized.

## Common Causes of HTTP 401

Common causes include:

- Expired access tokens
- Invalid access tokens
- Incorrect token audience
- Incorrect client configuration
- Missing authentication configuration
- Incorrect redirect URI configuration
- Missing environment variables required for authentication

## Authentication Investigation Procedure

When investigating a 401 response:

1. Check whether the access token has expired.
2. Validate the token audience against the expected application identifier.
3. Verify that the client identifier and tenant configuration are correct.
4. Verify that the configured redirect URI matches the registered redirect URI.
5. Check whether required authentication environment variables are available to the application.
6. Review application logs for authentication-related errors.
7. Confirm that the request is reaching the expected application instance.

## Token Audience

The token audience identifies the intended recipient of an access token.

An audience mismatch can cause an otherwise valid token to be rejected by the application.

## Configuration Changes

When an authentication failure begins immediately after a configuration or domain change, compare the authentication configuration before and after the change.

Relevant configuration includes:

- Client ID
- Tenant ID
- Redirect URI
- Token audience
- Authentication environment variables

## Escalation

If configuration appears correct but authentication continues to fail, capture:

- Request timestamp
- HTTP status code
- Relevant application logs
- Authentication configuration values excluding secrets
- Token claims excluding sensitive credentials

and escalate the issue to the platform or identity engineering team.