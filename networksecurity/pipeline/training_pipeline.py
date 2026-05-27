import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_transformation import DataTransformation,DataTransformationConfig
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.data_injestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig, ModelTrainerConfig
from networksecurity.entity.config_entity import (TrainingPipelineConfig,
                                                  DataIngestionConfig,
                                                  DataValidationConfig,
                                                  DataTransformationConfig,
                                                  ModelTrainerConfig)

from networksecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
    
    def start_data_injestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            logging.info("initiate data injestion")
            data_ingestion=DataIngestion(self.data_ingestion_config)
            data_injestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("data injestion completed")
            return data_injestion_artifact  
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info("initiate the data validation")    
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("data_validation_completed")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
            logging.info("initiate the data transformation")    
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info("data_transformation_completed")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=ModelTrainerConfig(self.training_pipeline_config)
            model_trainer=ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            logging.info("model training started")
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info("model training completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_training_pipeline(self):
        try:
            data_injestion_artifact=self.start_data_injestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_injestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)