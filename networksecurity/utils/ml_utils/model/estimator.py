

import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
class NetworkModel:
    def __init__(self,preprocessor,model,model_dir:str=SAVED_MODEL_DIR,model_file_name:str=MODEL_FILE_NAME):
        try:
            self.preprocessor=preprocessor
            self.model=model
            self.model_dir=model_dir
            self.model_file_name=model_file_name
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self,x):
        try:
            X_transformed=self.preprocessor.transform(x)
            y_pred=self.model.predict(X_transformed)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e,sys)