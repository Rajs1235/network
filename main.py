from networksecurity.components.data_injestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys
if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        data_injestion_config=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(data_injestion_config)
        logging.info("initiate data injestion")
        data_injestion_artifact=dataingestion.initiate_data_ingestion()
        print(data_injestion_artifact)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)