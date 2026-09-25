# Database Troubleshooting Guide

## Overview

Database issues can originate from connectivity, authentication, query performance, schema changes or resource constraints.

## Connectivity Investigation

When an application cannot connect to a database:

1. Verify the database endpoint.
2. Verify the database name.
3. Verify network connectivity.
4. Verify authentication configuration.
5. Verify firewall or network access rules.
6. Check application logs for connection errors.

## Query Performance

When database queries become slow:

1. Identify the slow query.
2. Review execution plans.
3. Check indexes.
4. Check for expensive joins.
5. Check for large scans.
6. Check database resource utilization.
7. Review recent schema or query changes.

## Connection Failures

Common causes include:

- Incorrect connection string
- Invalid credentials
- Network restrictions
- Database unavailable
- Connection pool exhaustion

## Production Safety

Database troubleshooting should avoid destructive operations unless explicitly approved.

Before modifying production data:

- Confirm the target environment.
- Confirm the affected objects.
- Review the intended operation.
- Obtain required approval.
- Prefer reversible operations where possible.