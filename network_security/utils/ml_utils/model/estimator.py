from network_security.constants.training_pipline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os
import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger


class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def predict(self,X):
        try:
            X_transformed = self.preprocessor.transform(X)
            y_hat = self.model.predict(X_transformed)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e