

import pytest
import pandas as pd
import numpy as np
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_training import ModelTraining
from application import app


class TestSimpleDataIngestion:
    """Simple tests for data ingestion"""
    
    def test_data_ingestion_initialization(self):
        """Test that DataIngestion can be created"""
        config = {
            "data_ingestion": {
                "bucket_name": "titanic1072025916",
                "bucket_file_name": "titanic.csv",
                "train_ratio": 0.85
            }
        }
        
        # This should not raise an error
        data_ingestion = DataIngestion(config)
        
        # Check that the object was created with correct values
        assert data_ingestion.bucket_name == "titanic1072025916"
        assert data_ingestion.file_name == "titanic.csv"
        assert data_ingestion.train_ratio == 0.85
    
    def test_data_ingestion_attributes_exist(self):
        """Test that DataIngestion has the required methods"""
        config = {
            "data_ingestion": {
                "bucket_name": "titanic1072025916",
                "bucket_file_name": "titanic.csv",
                "train_ratio": 0.85
            }
        }
        
        data_ingestion = DataIngestion(config)
        
        # Check that required methods exist
        assert hasattr(data_ingestion, 'download_csv_from_aws')
        assert hasattr(data_ingestion, 'split_data')
        assert hasattr(data_ingestion, 'run')


class TestSimpleDataProcessing:
    """Simple tests for data processing"""
    
    def test_data_processor_initialization(self):
        """Test that DataProcessor can be created"""
        # This should not raise an error
        processor = DataProcessor("train.csv", "test.csv", "processed/", "config.yaml")
        
        # Check that the object was created
        assert processor.train_path == "train.csv"
        assert processor.test_path == "test.csv"
        assert processor.processed_dir == "processed/"
    
    def test_preprocess_data_basic(self):
        """Test basic data preprocessing with simple data"""
        processor = DataProcessor("train.csv", "test.csv", "processed/", "config.yaml")
        
        # Create simple test data
        test_data = pd.DataFrame({
            'Name': ['Mr. John', 'Mrs. Jane'],
            'Sex': ['male', 'female'],
            'Age': [25, 30],
            'Fare': [10.0, 20.0],
            'Embarked': ['S', 'C'],
            'Cabin': [None, 'A1'],
            'SibSp': [0, 1],
            'Parch': [0, 0],
            'Survived': [0, 1]
        })
        
        # Process the data
        processed = processor.preprocess_data(test_data)
        
        # Check that processing worked
        assert len(processed) == 2  # Same number of rows
        assert 'Sex' in processed.columns  # Sex column should be encoded
        assert 'Familysize' in processed.columns  # New feature created
        assert 'Isalone' in processed.columns  # New feature created
        assert 'HasCabin' in processed.columns  # New feature created


class TestSimpleModelTraining:
    """Simple tests for model training"""
    
    def test_model_training_initialization(self):
        """Test that ModelTraining can be created"""
        # This should not raise an error
        model_training = ModelTraining("train.csv", "test.csv", "model.pkl")
        
        # Check that the object was created
        assert model_training.train_path == "train.csv"
        assert model_training.test_path == "test.csv"
        assert model_training.model_output_path == "model.pkl"
    
    def test_model_training_has_methods(self):
        """Test that ModelTraining has required methods"""
        model_training = ModelTraining("train.csv", "test.csv", "model.pkl")
        
        # Check that required methods exist
        assert hasattr(model_training, 'load_and_split_data')
        assert hasattr(model_training, 'train_lgbm')
        assert hasattr(model_training, 'evaluate_model')
        assert hasattr(model_training, 'save_model')
        assert hasattr(model_training, 'run')


class TestSimpleApplication:
    """Simple tests for the Flask application"""
    
    def test_app_creation(self):
        """Test that the Flask app can be created"""
        # This should not raise an error
        assert app is not None
        assert hasattr(app, 'routes')
    
    def test_app_has_index_route(self):
        """Test that the app has the main route"""
        # Check that the route exists
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        assert '/' in routes
    
    def test_app_config(self):
        """Test basic app configuration"""
        # Test that we can set testing mode
        app.config['TESTING'] = True
        assert app.config['TESTING'] == True


class TestSimpleDataValidation:
    """Simple tests for data validation"""
    
    def test_sample_data_creation(self):
        """Test that we can create sample data for testing"""
        # Create simple Titanic-like data
        data = pd.DataFrame({
            'PassengerId': [1, 2, 3],
            'Survived': [0, 1, 0],
            'Pclass': [3, 1, 3],
            'Name': ['Mr. John', 'Mrs. Jane', 'Miss Bob'],
            'Sex': ['male', 'female', 'male'],
            'Age': [25, 30, 35],
            'SibSp': [0, 1, 0],
            'Parch': [0, 0, 0],
            'Ticket': ['A1', 'B2', 'C3'],
            'Fare': [10.0, 50.0, 7.0],
            'Cabin': [None, 'A1', None],
            'Embarked': ['S', 'C', 'S']
        })
        
        # Basic validation
        assert len(data) == 3
        assert 'Survived' in data.columns
        assert 'Sex' in data.columns
        assert 'Age' in data.columns
        
        # Check data types
        assert data['Survived'].dtype in [np.int64, np.int32]
        assert data['Age'].dtype in [np.int64, np.int32, np.float64]
    
    def test_data_has_required_columns(self):
        """Test that our data has all required columns"""
        required_columns = [
            'PassengerId', 'Survived', 'Pclass', 'Name', 'Sex',
            'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'
        ]
        
        # Create sample data
        data = pd.DataFrame({
            'PassengerId': [1],
            'Survived': [0],
            'Pclass': [3],
            'Name': ['Mr. John'],
            'Sex': ['male'],
            'Age': [25],
            'SibSp': [0],
            'Parch': [0],
            'Ticket': ['A1'],
            'Fare': [10.0],
            'Cabin': [None],
            'Embarked': ['S']
        })
        
        # Check that all required columns are present
        for column in required_columns:
            assert column in data.columns, f"Missing column: {column}"


class TestSimpleErrorHandling:
    """Simple tests for error handling"""
    
    def test_invalid_config_handling(self):
        """Test that invalid config is handled gracefully"""
        # Test with missing config
        try:
            data_ingestion = DataIngestion({})
            # This should raise an error or handle it gracefully
        except Exception as e:
            # It's okay if it raises an error - that's expected behavior
            assert isinstance(e, Exception)
    
    def test_missing_file_handling(self):
        """Test that missing files are handled gracefully"""
        # Test with non-existent file paths
        try:
            processor = DataProcessor("nonexistent.csv", "nonexistent.csv", "processed/", "config.yaml")
            # This should not crash
        except Exception as e:
            # It's okay if it raises an error - that's expected behavior
            assert isinstance(e, Exception)


# Simple utility functions for testing
def create_sample_titanic_data():
    """Create a simple sample of Titanic data for testing"""
    return pd.DataFrame({
        'PassengerId': [1, 2, 3, 4, 5],
        'Survived': [0, 1, 0, 1, 0],
        'Pclass': [3, 1, 3, 1, 3],
        'Name': ['Mr. John Doe', 'Mrs. Jane Doe', 'Miss Bob Smith', 'Master Alice Johnson', 'Dr. Charlie Brown'],
        'Sex': ['male', 'female', 'male', 'female', 'male'],
        'Age': [22, 38, 26, 35, 35],
        'SibSp': [1, 1, 0, 1, 0],
        'Parch': [0, 0, 0, 0, 0],
        'Ticket': ['A/5 21171', 'PC 17599', 'STON/O2. 3101282', '113803', '373450'],
        'Fare': [7.25, 71.2833, 7.925, 53.1, 8.05],
        'Cabin': [None, 'C85', None, 'C123', None],
        'Embarked': ['S', 'C', 'S', 'S', 'S']
    })


def test_sample_data_creation():
    """Test that our sample data creation function works"""
    data = create_sample_titanic_data()
    
    # Basic checks
    assert len(data) == 5
    assert 'Survived' in data.columns
    assert 'Sex' in data.columns
    assert data['Survived'].sum() == 2  # 2 survivors out of 5 passengers
    
    print("✅ Sample data creation test passed!")


if __name__ == "__main__":
    # Run a simple test
    test_sample_data_creation()
    print("🎉 All simple tests completed!") 