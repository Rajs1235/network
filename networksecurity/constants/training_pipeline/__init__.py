import os
import sys
import numpy as np
import pandas as pd


TARGET_COLUMN = "Status"
PIPELINE_NAME = "network_security"
ARTIFACT_DIR = "artifact"
FILE_NAME = "data.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_scheme", "schema.yaml")

DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DATABASE_DIR_NAME = "NetworkData"
DATA_INGESTION_DATABASE_COLLECTION_NAME = "NetworkSecurity"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR_NAME = "feature_store"
DATA_INGESTION_INGESTED_DIR_NAME = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yaml"