import yaml
from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger
import os, sys
import numpy as np
import pandas as pd
import dill
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
