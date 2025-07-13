#!/usr/bin/env python3
"""
Simple test runner for beginners.
This script runs basic tests to help you understand testing.
"""

import subprocess
import sys
import os


def run_simple_test():
    """Run a simple test to check if everything is working"""
    print("🧪 Running simple tests...")
    print("=" * 40)
    
    try:
        # Test 1: Check if we can import our modules
        print("1. Testing imports...")
        import pandas as pd
        import numpy as np
        print("   ✅ pandas and numpy imported successfully")
        
        # Test 2: Check if our source code exists
        print("2. Checking source files...")
        required_files = [
            "src/data_ingestion.py",
            "src/data_processing.py", 
            "src/model_training.py",
            "application.py"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"   ✅ {file} exists")
            else:
                print(f"   ❌ {file} missing")
                return False
        
        # Test 3: Run the simple test file
        print("3. Running simple tests...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_simple.py", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Simple tests passed!")
            print(result.stdout)
        else:
            print("   ❌ Some tests failed!")
            print(result.stdout)
            print(result.stderr)
            return False
        
        print("\n🎉 All simple tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_individual_test(test_name):
    """Run a specific test by name"""
    print(f"🧪 Running test: {test_name}")
    print("=" * 40)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            f"tests/test_simple.py::{test_name}", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Test passed!")
            print(result.stdout)
        else:
            print("❌ Test failed!")
            print(result.stdout)
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running test: {e}")
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
    """Main function"""
    print("🚢 Titanic Survival Prediction - Simple Test Runner")
    print("=" * 50)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("\nUsage:")
            print("  python run_simple_tests.py                    # Run all tests")
            print("  python run_simple_tests.py --class <name>     # Run specific test class")
            print("  python run_simple_tests.py --list             # Show available tests")
            return
        
        elif sys.argv[1] == "--list":
            show_available_tests()
            return
        
        elif sys.argv[1] == "--class" and len(sys.argv) > 2:
            test_class = sys.argv[2]
            success = run_individual_test(test_class)
            sys.exit(0 if success else 1)
    
    # Run all tests by default
    success = run_simple_test()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 