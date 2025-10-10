import sys
import os

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constants.training_pipline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.constants.training_pipline import TARGET_COLUMN

from network_security.entity.artifict_entity import (
    DataTransformationArtifact,
    DataIngestionArtifact
)
from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger
from network_security.utils.main_utils.utils import save_numpy_array_data, save_object