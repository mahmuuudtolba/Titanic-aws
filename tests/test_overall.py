import pytest
import pandas as pd
import numpy as np
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_training import ModelTraining
from application import app


class TestDataIngestion:
    """Test data ingestion"""
    def test_data_ingestion_initialization(self):
        config = {
            "data_ingestion": {
                "bucket_name": "titanic1072025916",
                "file_name": "titanic.csv",
                "train_ratio": 0.85
            }
        }

        data_ingestion = DataIngestion(config)
        assert data_ingestion.bucket_name == "titanic1072025916"
        assert data_ingestion.file_name == "titanic.csv"
        assert data_ingestion.train_ratio == 0.85

    def test_data_ingestion_exits(self):
        config = {
            "data_ingestion": {
                "bucket_name": "titanic1072025916",
                "file_name": "titanic.csv",
                "train_ratio": 0.85
            }
        }

        data_ingestion = DataIngestion(config)
        assert hasattr(data_ingestion , "download_csv_from_aws")
        assert hasattr(data_ingestion , "split_data")
        assert hasattr(data_ingestion , "run")
