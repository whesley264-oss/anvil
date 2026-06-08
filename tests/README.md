# ANVIL Tests

## Overview

This directory contains tests for the ANVIL CLI project.

## Structure

```
tests/
├── test_anvil.py           # Main test file
├── requirements_test.txt   # Test dependencies
└── README.md              # This file
```

## Running Tests Locally

### Install dependencies:
```bash
cd tests
pip install -r requirements_test.txt
```

### Run tests:
```bash
python test_anvil.py
```

## GitHub Actions CI/CD Pipeline

The `.github/workflows/ci.yml` file defines a complete CI/CD pipeline:

### Jobs:

1. **Lint** - Code quality checks (Black, isort, flake8)
2. **Unit Tests** - Core functionality tests
3. **CLI Integration Tests** - Test all CLI commands
4. **Build Demo APK** - Build a real APK to verify everything works
5. **Security Scan** - Bandit security checks
6. **Performance** - Benchmark CLI startup time
7. **Release** - Auto-create release on git tags

### Running locally before pushing:

```bash
# Test your changes
cd tests
python test_anvil.py

# Test CLI manually
anvil --help
anvil --version
anvil doctor
```

## Test Coverage

- Banner import
- Config validation
- Package name validation
- Generator imports
- Gradle files generation
- CLI command execution
- APK build process (via GitHub Actions)

## Adding New Tests

Add test functions to `test_anvil.py`:

```python
def test_my_new_feature():
    """Test description"""
    # Your test code
    assert something == expected
    print("✓ My new feature test passed")
```

Then add it to `run_all_tests()` function.