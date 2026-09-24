# Engineering Standards

## Code Quality

Engineering code should be:

- Readable
- Maintainable
- Tested
- Version controlled
- Documented where necessary

## Configuration

Configuration should be separated from application code.

Secrets must not be committed to source control.

Environment-specific configuration should be managed separately.

## Logging

Applications should produce useful operational logs without exposing:

- Passwords
- Access tokens
- API keys
- Connection secrets

## Testing

Changes should include appropriate automated tests.

Critical production workflows should have smoke tests.

## Version Control

Changes should be committed using meaningful messages.

Large changes should be reviewed before merging.

## Documentation

Operationally important behavior should be documented so that another engineer can troubleshoot the system without relying entirely on the original developer.