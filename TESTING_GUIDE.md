# 🧪 Simple Testing Guide

This guide will help you understand testing step by step.

## What is Testing?

Testing is like checking if your code works correctly. Think of it like:
- **Unit Tests**: Testing individual pieces (like testing if a function works)
- **Integration Tests**: Testing how pieces work together
- **Application Tests**: Testing the whole application

## Quick Start

### 1. Run Simple Tests
```bash
python run_simple_tests.py
```

### 2. Run Specific Tests
```bash
# Run all simple tests
pytest tests/test_simple.py -v

# Run a specific test class
pytest tests/test_simple.py::TestSimpleDataIngestion -v

# Run a specific test method
pytest tests/test_simple.py::TestSimpleDataIngestion::test_data_ingestion_initialization -v
```

### 3. See Available Tests
```bash
python run_simple_tests.py --list
```

## Understanding the Tests

### Test Structure
```python
class TestSimpleDataIngestion:
    """Simple tests for data ingestion"""
    
    def test_data_ingestion_initialization(self):
        """Test that DataIngestion can be created"""
        # Arrange: Set up your test data
        config = {
            "data_ingestion": {
                "bucket_name": "test-bucket",
                "bucket_file_name": "test.csv",
                "train_ratio": 0.8
            }
        }
        
        # Act: Do the thing you want to test
        data_ingestion = DataIngestion(config)
        
        # Assert: Check if the result is what you expect
        assert data_ingestion.bucket_name == "test-bucket"
        assert data_ingestion.file_name == "test.csv"
        assert data_ingestion.train_ratio == 0.8
```

### What Each Part Does:
1. **Arrange**: Set up your test data
2. **Act**: Run the code you want to test
3. **Assert**: Check if the result is correct

## Test Categories

### 1. Data Ingestion Tests
- Tests if we can create the DataIngestion class
- Tests if it has the right methods
- Tests if it can handle configuration

### 2. Data Processing Tests
- Tests if we can create the DataProcessor class
- Tests if data preprocessing works
- Tests if new features are created correctly

### 3. Model Training Tests
- Tests if we can create the ModelTraining class
- Tests if it has the required methods
- Tests if it can handle training data

### 4. Application Tests
- Tests if the Flask app can be created
- Tests if it has the right routes
- Tests if it can handle configuration

### 5. Data Validation Tests
- Tests if we can create sample data
- Tests if data has the right columns
- Tests if data types are correct

### 6. Error Handling Tests
- Tests if the code handles errors gracefully
- Tests if it doesn't crash with bad input

## Writing Your Own Tests

### Step 1: Create a Test Function
```python
def test_my_function():
    """Test that my function works correctly"""
    # Arrange
    input_data = "test"
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == "expected_output"
```

### Step 2: Test Different Scenarios
```python
def test_my_function_with_different_inputs():
    """Test my function with different inputs"""
    # Test case 1
    assert my_function("hello") == "expected1"
    
    # Test case 2
    assert my_function("world") == "expected2"
    
    # Test case 3 - edge case
    assert my_function("") == "expected3"
```

### Step 3: Test Error Cases
```python
def test_my_function_with_bad_input():
    """Test that my function handles errors correctly"""
    try:
        result = my_function(None)  # This should cause an error
        assert False, "Should have raised an error"
    except Exception as e:
        # This is expected - the function should handle the error
        assert isinstance(e, Exception)
```

## Common Assertions

```python
# Check if values are equal
assert result == expected_value

# Check if something is True
assert condition == True

# Check if something is False
assert condition == False

# Check if something is None
assert result is None

# Check if something is not None
assert result is not None

# Check if a list contains something
assert item in my_list

# Check if a string contains something
assert "text" in my_string

# Check if an object has an attribute
assert hasattr(my_object, 'attribute_name')

# Check if a file exists
import os
assert os.path.exists("file.txt")
```

## Running Tests

### Basic Commands
```bash
# Run all tests
pytest

# Run tests with more detail
pytest -v

# Run tests and show print statements
pytest -s

# Run tests and stop on first failure
pytest -x

# Run tests and show local variables on failure
pytest -l
```

### Running Specific Tests
```bash
# Run tests in a specific file
pytest tests/test_simple.py

# Run a specific test class
pytest tests/test_simple.py::TestSimpleDataIngestion

# Run a specific test method
pytest tests/test_simple.py::TestSimpleDataIngestion::test_data_ingestion_initialization

# Run tests that match a pattern
pytest -k "data"
```

## Understanding Test Output

### ✅ Passing Test
```
test_simple.py::TestSimpleDataIngestion::test_data_ingestion_initialization PASSED
```

### ❌ Failing Test
```
test_simple.py::TestSimpleDataIngestion::test_data_ingestion_initialization FAILED
```

### Error Details
When a test fails, pytest shows:
- What was expected vs what was actually returned
- The line where the test failed
- The values of variables at the time of failure

## Tips for Beginners

1. **Start Simple**: Write basic tests first
2. **Test One Thing**: Each test should test one specific thing
3. **Use Descriptive Names**: Test names should explain what you're testing
4. **Test Both Success and Failure**: Test what happens when things go wrong
5. **Keep Tests Independent**: Each test should not depend on other tests

## Next Steps

Once you're comfortable with simple tests, you can:
1. Add more test cases
2. Test edge cases (unusual inputs)
3. Test error conditions
4. Add integration tests
5. Add performance tests

## Need Help?

- Check the test output for error messages
- Add print statements to see what's happening
- Use `pytest -s` to see print statements
- Use `pytest -l` to see local variables on failure

Remember: Testing is a skill that takes practice. Start simple and build up gradually! 🚀 