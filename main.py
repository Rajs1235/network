from networksecurity.components.data_injestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation,DataTransformationConfig
from networksecurity.components.model_trainer import ModelTrainer
import os
import sys
import warnings

warnings.filterwarnings("ignore")

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        data_injestion_config=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(data_injestion_config)
        logging.info("initiate data injestion")
        data_injestion_artifact=dataingestion.initiate_data_ingestion()
        logging.info("data injestion completed")
        data_validation_config=DataValidationConfig(trainingpipelineconfig)        
        data_validation=DataValidation(data_injestion_artifact,data_validation_config)
        logging.info("initiate the data validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data_validation_completed")
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("data Transformation completed")

        logging.info("model training started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config,data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("model training completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)