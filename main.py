from network_security.components.data_ingection import DataIngestion
from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger
from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataTransformationConfig
from network_security.entity.config_entity import DataValidationConfig
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.utils.main_utils.utils import load_numpy_array_data,save_numpy_array_data
from network_security.components.model_trainer import ModelTrainer
from network_security.entity.artifict_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from network_security.entity.config_entity import ModelTrainerConfig
import os
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logger.logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logger.logging.info("Data Initiation Completed")
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logger.logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logger.logging.info("data Validation Completed")
        print(data_validation_artifact)
        logger.logging.info("Initiate the Data Transformation")
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logger.logging.info("Data Transformation Completed")
        logger.logging.info("model training artifect started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

    except Exception as e:
           raise NetworkSecurityException(e,sys)