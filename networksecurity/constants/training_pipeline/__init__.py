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


DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DATABASE_DIR_NAME = "NetworkData"
DATA_INGESTION_DATABASE_COLLECTION_NAME = "NetworkSecurity"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR_NAME = "feature_store"
DATA_INGESTION_INGESTED_DIR_NAME = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2