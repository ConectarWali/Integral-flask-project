## Testing

The library includes a comprehensive test suite. To run the tests:

```bash
python -m unittest discover tests
```

### Test Structure

The test suite is organized into several test classes:

1. **TestIntegralFlaskProject**
   - Tests the main application class
   - Verifies singleton pattern
   - Tests property access
   - Tests blueprint creation
   - Tests different run modes
   - Tests module importing

2. **TestCORSManager**
   - Tests CORS configuration creation
   - Tests endpoint discovery
   - Tests header application
   - Tests CORS rules application

3. **TestConfig**
   - Tests default configuration values
   - Tests environment-specific configurations
   - Tests configuration overrides
   - Tests different configuration components (DB, Mail, JWT, SocketIO)

4. **TestModuleImporter**
   - Tests single module importing
   - Tests nested module importing
   - Tests error handling
   - Tests empty package handling

### Writing New Tests

When adding new features, please ensure to add corresponding tests. Example:

```python
from unittest import TestCase
from integral_flask_project import Integral_flask_project

class TestNewFeature(TestCase):
    def setUp(self):
        self.app = Integral_flask_project(__name__)

    def test_feature(self):
        result = self.app.new_feature()
        self.assertEqual(result, expected_value)
```

### Test Coverage

To generate a test coverage report:

```bash
coverage run -m unittest discover
coverage report
coverage html  # For detailed HTML report
```

Target test coverage: 90% or higher

### Running Specific Tests

Run specific test classes:
```bash
python -m unittest tests.test_cors_manager.TestCORSManager
```

Run specific test methods:
```bash
python -m unittest tests.test_cors_manager.TestCORSManager.test_create_config
```