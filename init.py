from os.path import join, dirname
import yaml


def load_config(path='config.prod.yml'):
    path = join(dirname(__file__), path)
    with open(path) as file:
        return yaml.load(file)
