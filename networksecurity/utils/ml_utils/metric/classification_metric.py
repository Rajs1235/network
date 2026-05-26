from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.entity.config_entity import ClassificationMetricConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        f1_score_value=f1_score(y_true,y_pred,pos_label="phishing",zero_division=0)
        precision_score_value=precision_score(y_true,y_pred,pos_label="phishing",zero_division=0)
        recall_score_value=recall_score(y_true,y_pred,pos_label="phishing",zero_division=0)
        classification_metric_artifact=ClassificationMetricArtifact(
            f1_score=f1_score_value,
            precision_score=precision_score_value,
            recall_score=recall_score_value
        )
        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)