import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_data , read_yaml



logger = get_logger(__name__)

class DataProcessor:
    def __init__(self , train_path , test_path , processed_dir , config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(CONFIG_PATH)

        os.makedirs(self.processed_dir , exist_ok=True)


    def preprocess_data(self , df):
        try:
            df['Age'] = df['Age'].fillna(df['Age'].median())
            df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
            df['Fare'] = df['Fare'].fillna(df['Fare'].median())
            df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
            df['Embarked'] = df['Embarked'].astype('category').cat.codes


            df['Familysize'] = df['SibSp'] + df['Parch'] + 1

            df['Isalone'] = (df['Familysize'] == 1).astype(int)

            df['HasCabin'] = df['Cabin'].notnull().astype(int)

            df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False).map(
                {'Mr': 0, 'Miss': 1, 'Mrs': 2, 'Master': 3, 'Rare': 4}
            ).fillna(4)

            df['Pclass_Fare'] = df['Pclass'] * df['Fare']
            df['Age_Fare'] = df['Age'] * df['Fare']

            

            logger.info("Data Preprocessing done...")


            return df

        except Exception as e:
            logger.error(f"Error while preprocessing data {e}")
            raise CustomException(str(e) , e)
        


    def handle_imbalance_data(self ,df):
        try:
            X = df[['Pclass', 'Sex', 'Age', 'Fare', 'Embarked', 'Familysize', 'Isalone', 'HasCabin', 'Title', 'Pclass_Fare', 'Age_Fare']]
            y = df['Survived']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            balanced_df = pd.DataFrame(X_resampled , columns=X.columns)
            balanced_df["Survived"] = y_resampled

            logger.info("Data balanced sucesffuly")
            return balanced_df
        
        except Exception as e:

            logger.error(f"Error during balancing data step {e}")
            raise CustomException("Error while balancing data", e)
        

    def save_data(self , df , file_path):
        try:
            logger.info("saving our data in processed folder")
            df.to_csv(file_path , index= False)
            logger.info(f"Data saved successfully to {file_path}")

        except Exception as e :
            logger.error(f"Error during saving data {e}")
            raise CustomException("Error during saving data " , e)
        

    def process(self):
        try:
            logger.info("Loading data from RAW directory")
            df_train = read_data(self.train_path)
            df_test = read_data(self.test_path)

            df_train = self.preprocess_data(df_train )
            df_test = self.preprocess_data(df_test)

            df_train = df_train[self.config['data_processing']['selected_features']]
            df_test = df_test[self.config['data_processing']['selected_features']]


            df_train = self.handle_imbalance_data(df_train )
            


            df_train = self.save_data(df_train , PROCESSED_TRAIN_DATA_PATH)
            df_test = self.save_data(df_test , PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except Exception as e :
            logger.error(f"Error during preprocessing pipeline {e}")
            raise CustomException("Error during preprocessing pipeline" , e)
        
if __name__=="__main__":
    data_processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR , CONFIG_PATH)
    data_processor.process()

        


