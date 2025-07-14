import subprocess
import sys
import os

def run_tests():
    """Run tests to if everything is working"""
    print("🧪 Running tests...")
    print("=" * 40)


    try:
        # Test 1 : Check if we can import our modules
        print("1. Testing imports...")
        import pandas as pd
        import numpy as np

        print("   ✅ pandas and numpy imported successfully")

        # Test 2 : Check if our source files exist
        print("2. Checking source files...")
        required_files = [
            "src/data_ingestion.py",
            "src/data_processing.py",
            "src/model_training.py",
            "pipeline/training_pipeline.py",
            "Dockerfile",
            "application.py"
        ]

        for file in required_files:
            if os.path.exists(file):
                print(f"   ✅ {file} exists")
            else:
                print(f"   ❌ {file} missing")
                return False


        # Test 3 : Run the test file
        print("3. Running test file...")
        result = subprocess.run([
            sys.executable , # the same Python interpreter running the script
            "-m" , 
            "pytest" , 
            "tests/test_overall.py",
            "-v",
            "--tb=short" ],
            capture_output=True,text=True)
        
        if result.returncode == 0:
            print("   ✅ Test file passed!")
            print(result.stdout)
        else:
            print("   ❌ Some tests failed!")
            print(result.stdout)
            return False

    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False
        
def show_available_tests():
    """Show all available tests"""
    print("📋 Available tests:")
    print("=" * 40)
    
    test_classes = [
        "TestSimpleDataIngestion",
        "TestSimpleDataProcessing", 
        "TestSimpleModelTraining",
        "TestSimpleApplication",
        "TestSimpleDataValidation",
        "TestSimpleErrorHandling"
    ]
    
    for i, test_class in enumerate(test_classes, 1):
        print(f"{i}. {test_class}")
    
    print("\nTo run a specific test class:")
    print("python run_simple_tests.py --class TestSimpleDataIngestion")
    
    print("\nTo run all tests:")
    print("python run_simple_tests.py")


def main():
    """Main function to run the tests"""
    print("🧪 Running tests...")
    print("=" * 40)


    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            show_available_tests()
            return
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("\nUsage:")
            print("  python run_simple_tests.py                    # Run all tests")
            print("  python run_simple_tests.py --class <name>     # Run specific test class")
            print("  python run_simple_tests.py --list             # Show available tests")
            return
        
    # Run all tests by default
    success = run_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()   