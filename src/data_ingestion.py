import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml
import boto3


logger = get_logger(__name__)

class DataIngestion:
    def __init__(self , config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]


        os.makedirs(RAW_DIR , exist_ok=True)
        logger.info(f"Data ingestions started with {self.bucket_name} with {self.file_name}")



    def download_csv_from_aws(self):
        try:

            client = boto3.client('s3')
            client.download_file(self.bucket_name , self.file_name , RAW_FILE_PATH)
            logger.info(f"Raw file is successfully downloaded to {RAW_FILE_PATH}")


        except Exception as e :

            logger.error("Error while Downloading csv file")
            raise CustomException("Failed to Download csv" , e)
        

    def split_data(self):
        try : 
            logger.info("Start the splitting process")
            data = pd.read_csv(RAW_FILE_PATH)
            X = data.drop(columns='Survived')
            y = data["Survived"]
            train_data, test_data = train_test_split(data , train_size= self.train_ratio , stratify=y)  

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"Traind data saved to {TRAIN_FILE_PATH}") 
            logger.info(f"Test data saved to {TEST_FILE_PATH}")    

        except Exception as e :
            logger.error("Error while Splitting data")
            raise CustomException("Failed to split data into training and test sets" , e)


    def run(self):
        try :
            logger.info("Starting data ingestion process")
            self.download_csv_from_aws()
            self.split_data()
            logger.info("Data ingestion completed successfully")
        except CustomException as e :
            logger.error("Error while ingesting data")
            raise CustomException("Failed to ingest data" , e)
        

        finally:
            logger.info("Data ingestion completed")


if __name__ == "__main__" :
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
