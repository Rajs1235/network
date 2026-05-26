from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys,os
import numpy as np
import pickle
import dill
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path:str,data:dict):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as yaml_file:
            yaml.dump(data,yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(file_path:str,array:np.array):
    try:
        logging.info(f"entered for Saving numpy array data to file: {file_path}")
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
        logging.info(f"exited after Saving numpy array data to file: {file_path}")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_obj(file_path:str,obj):
    try:
        logging.info(f"entered for Saving object file: {file_path}")
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info(f"exited after Saving object file: {file_path}")
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def load_obj(file_path:str,)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"file: {file_path} does not exist")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return dill.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj, allow_pickle=True)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
def evaluate_classification_model(X_train,y_train,X_test,y_test,models,params):
    try:
        report={}
        for i in range(len(models)):
            model_name=list(models.keys())[i]
            model=list(models.values())[i]
            para=params[model_name]
            logging.info(f"Starting model training and tuning for: {model_name}")
            gs=GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)
            train_model_score=accuracy_score(y_train,y_train_pred)
            test_model_score=accuracy_score(y_test,y_test_pred)
            report[model_name]={
                "train_score":train_model_score,
                "test_score":test_model_score
            }
            logging.info(f"Completed {model_name} with train_score={train_model_score}, test_score={test_model_score}")
        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e