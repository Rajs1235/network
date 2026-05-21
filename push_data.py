import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()


mongo_uri = os.getenv("MONGO_DB_URL")
print(f"Mongo URI: {mongo_uri}")

import certifi
# to make a secure connection to MongoDB Atlas, 
# we need to specify the path to the CA certificate bundle
ca=certifi.where()#certificate authorities

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def cv_to_json_convertor(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records=list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_records_to_mongodb(self,records,database,collection):
        try:
            if not records:
                raise ValueError("No records found to insert into MongoDB")
            self.database=database
            self.collection=collection
            self.records=records
            self.client = pymongo.MongoClient(os.getenv("MONGO_DB_URL"), tlsCAFile=ca)

            self.database = self.client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    FILE_PATH="Network_Data/data.csv"
    DATABASE="NetworkSecurity"
    COLLECTION="NetworkData"
    NETWORK_DATA_EXTRACT=NetworkDataExtract()
    records=NETWORK_DATA_EXTRACT.cv_to_json_convertor(FILE_PATH)
    print(records)
    no_of_records=NETWORK_DATA_EXTRACT.insert_records_to_mongodb(records,DATABASE,COLLECTION)
    print(no_of_records)
