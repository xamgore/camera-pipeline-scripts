from os.path import join, dirname
from typing import Dict, Any

import yaml


def load(path: str = 'config.prod.yml') -> Dict[str, Any]:
    """
    :param path: relative to the repository root
    :return: dictionary with the environment variables
    """
    path = join(dirname(__file__), path)
    with open(path) as file:
        return yaml.load(file)
