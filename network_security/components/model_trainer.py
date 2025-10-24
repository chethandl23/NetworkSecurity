import os
import sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger

from network_security.entity.artifict_entity import DataTransformationArtifact,ModelTrainerArtifact
from network_security.entity.config_entity import ModelTrainerConfig

from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.main_utils.utils import save_object,load_object
from network_security.utils.main_utils.utils import load_numpy_array_data,save_numpy_array_data,evaluate_model
from network_security.utils.ml_utils.metric.classification_metric import get_classification_scores

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier


class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def train_model(self,X_train, y_train,X_test, y_test) -> NetworkModel:
        try:
            models = {
                "LogisticRegression": LogisticRegression(),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "RandomForestClassifier": RandomForestClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(),
                "AdaBoostClassifier": AdaBoostClassifier()
            }
            params = {
                "DecisionTreeClassifier": {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                    'max_depth': [3, 5, 10, 20, None]
                },
                "RandomForestClassifier": {
                    'n_estimators': [50, 100, 200],
                    # 'criterion': ['gini', 'entropy', 'log_loss'],
                    # 'max_depth': [3, 5, 10, 20, None]
                },
                "GradientBoostingClassifier": {
                    'learning_rate': [0.01, 0.1, 0.2],
                    'n_estimators': [50, 100, 200]
                },
                "AdaBoostClassifier": {
                    'learning_rate': [0.01, 0.1, 0.2],
                    'n_estimators': [50, 100, 200]
                },
                "LogisticRegression": {},
                "KNeighborsClassifier": {}
            }

            model_report :dict = evaluate_model(X_train=X_train, y_train=y_train,
                                                X_test=X_test, y_test=y_test,
                                                models=models, params=params)
            # to get the best model score from dict
            # Choose the metric you want to compare — usually test_score or accuracy
            best_model_name = max(model_report, key=lambda x: model_report[x]["test_score"])
            best_model_score = model_report[best_model_name]["test_score"]

            logger.logging.info(f"Best found model on both training and testing dataset is {best_model_name} with score {best_model_score}")
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            classification_train_metric = get_classification_scores(y_true=y_train, y_pred=y_train_pred)

            ## track the ml flow

            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_scores(y_true=y_test, y_pred=y_test_pred)

            preprocessor  = load_object(self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)

            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)
            
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            logger.logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            logger.logging.info(f"Loading transformed training array and testing array")
            # load numpy array data
            train_array = load_numpy_array_data(file_path=train_file_path)
            test_array = load_numpy_array_data(file_path=test_file_path)

            X_train, y_train , X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            model = self.train_model(X_train, y_train, X_test, y_test)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
