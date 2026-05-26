import os
import sys
import mlflow
from sklearn.linear_model import LogisticRegression
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_obj,save_numpy_array_data
from networksecurity.utils.main_utils.utils import load_obj,load_numpy_array_data,evaluate_classification_model
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,precision_score,recall_score,f1_score,r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier)

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def track_mlflow(self,best_model,classification_metric):
        with mlflow.start_run():
            f1_score=classification_metric.f1_score
            precision_score=classification_metric.precision_score
            recall_score=classification_metric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,artifact_path="model")
            

    def train_model(self,X_train,y_train,X_test,y_test):
        models={
            "Decision Tree":DecisionTreeClassifier(),
            "Random Forest":RandomForestClassifier(),
            "Gradient Boosting":GradientBoostingClassifier(),
            "AdaBoost":AdaBoostClassifier(),
            "Logistic Regression":LogisticRegression(),
        }
        params={
            "Decision Tree":{
                "criterion": ["gini", "entropy"],
                "splitter": ["best", "random"],
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 10],
                "min_samples_leaf": [1, 2]
            },
            "Random Forest":{
                "n_estimators": [100, 200],
                "criterion": ["gini", "entropy"],
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 10],
                "min_samples_leaf": [1, 2]
            },
            "Gradient Boosting":{
                "n_estimators": [100, 200],
                "learning_rate": [0.01, 0.1],
                "max_depth": [3, 5],
                "subsample": [0.8, 1.0]
            },
            "AdaBoost":{
                "n_estimators": [50, 100],
                "learning_rate": [0.1, 1.0]
            },
            "Logistic Regression":{
                "C": [0.1, 1.0, 10.0],
                "solver": ["lbfgs", "liblinear"],
                "max_iter": [100, 200]
            },
        }
        model_report:dict=evaluate_classification_model(models=models,X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,params=params)
        best_model_name=max(model_report, key=lambda model_name: model_report[model_name]["test_score"])
        best_model_score=model_report[best_model_name]["test_score"]
        best_model=models[best_model_name]
        logging.info(f"best model found on both training and testing dataset is {best_model_name} with accuracy score: {best_model_score}")
        y_train_pred=best_model.predict(X_train)
        y_test_pred=best_model.predict(X_test)
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
        self.track_mlflow(best_model,classification_train_metric)
        y_test_pred=best_model.predict(X_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)
        self.track_mlflow(best_model,classification_test_metric)

        preprocessor=load_obj(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)
        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_obj(self.model_trainer_config.trained_model_file_path,obj=Network_Model)
        # Model_Trainer_Artifact
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                            train_metric_artifact=classification_train_metric,
                            test_metric_artifact=classification_test_metric)
        
        logging.info(f"model trainer artifact created successfully")
        return model_trainer_artifact

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)
            X_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            X_test,y_test=test_arr[:,:-1],test_arr[:,-1]
            return self.train_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test)

        except Exception as e:
            raise NetworkSecurityException(e,sys)