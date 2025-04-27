# NZ Adventure Game

[![Test](https://github.com/[YOUR_USERNAME]/nz-adventure-terraform/actions/workflows/test.yml/badge.svg)](https://github.com/[YOUR_USERNAME]/nz-adventure-terraform/actions/workflows/test.yml)
[![Lint](https://github.com/[YOUR_USERNAME]/nz-adventure-terraform/actions/workflows/lint.yml/badge.svg)](https://github.com/[YOUR_USERNAME]/nz-adventure-terraform/actions/workflows/lint.yml)
[![Security](https://github.com/[YOUR_USERNAME]/nz-adventure-terraform/actions/workflows/security.yml/badge.svg)](https://github.com/[YOUR_USERNAME]/nz-adventure-terraform/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/[YOUR_USERNAME]/nz-adventure-terraform/branch/main/graph/badge.svg)](https://codecov.io/gh/[YOUR_USERNAME]/nz-adventure-terraform)

A text-based adventure game set in New Zealand, built with Flask and Firestore.

## Development Setup

1. Install dependencies:
```bash
pip install -e ".[dev]"
```

2. Set up environment variables:
```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
# For production
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
# For testing
export FIRESTORE_EMULATOR_HOST=localhost:8081
```

## Code Quality

This project uses several tools to ensure code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Style guide enforcement
- **mypy**: Static type checking

Run all checks locally:
```bash
black src tests
isort src tests
flake8 src tests
mypy src tests
```

## Security

We use multiple tools to ensure security:

- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability checking
- **Snyk**: Continuous security monitoring
- **Dependency Review**: PR dependency analysis

Run security checks locally:
```bash
bandit -r src/
safety check
```

## Running Tests

### Using the Firestore Emulator (Recommended)

1. Start the emulator:
```bash
./scripts/test_setup.sh start
```

2. Run the tests:
```bash
pytest
```

3. Stop the emulator:
```bash
./scripts/test_setup.sh stop
```

### Using Docker (Alternative)

You can also run the tests using Docker:

```bash
docker run -p 8081:8081 -e FIRESTORE_PROJECT_ID=test-project mtlynch/firestore-emulator
pytest
```

## CI/CD

This project uses GitHub Actions for continuous integration. On every push and pull request:
- Runs all tests against the Firestore emulator
- Performs code quality checks (linting, formatting)
- Runs security scans
- Generates and uploads test coverage reports

Additional security scans run weekly to check for new vulnerabilities.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass and linting is clean
5. Submit a pull request

## License

MIT 