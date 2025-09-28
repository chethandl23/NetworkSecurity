from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger


from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifict_entity import DataIngestionArtifact
import sys
import os
import pymongo
import pandas as pd
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGODB_URI")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_dataframe(self):
        #read the data from mongodb and store it in a dataframe
        try:
            data_base_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[data_base_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    # def export_data_into_feature_store(self,dataframe:pd.DataFrame):
    #     try:
    #         # feature_store_file_path = self.data_ingestion_config.feature_store_file_path
    #         dir_path = os.path.dirname(feature_store_file_path)
    #         os.makedirs(dir_path,exist_ok=True)
    #         dataframe.to_csv(feature_store_file_path,index=False,header=True)
    #         return dataframe
    #     except Exception as e:
    #         raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logger.logging.info("Successfully split the data into train and test")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok = True)

            logger.logging.info("Exporting training and testing data")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logger.logging.info("Exporting of training and testing data is completed")

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            # dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                # feature_store_file_path = self.data_ingestion_config.feature_store_file_path,
                trained_file_path = self.data_ingestion_config.training_file_path,
                test_file_path = self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact



        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

