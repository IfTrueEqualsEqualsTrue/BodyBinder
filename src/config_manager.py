import yaml
from yaml import load, dump, Loader
import json


def get_config(config_path):
    fichier = open(config_path, 'r')
    return load(fichier, Loader)


def save_config(config, config_path):
    fichier = open(config_path, 'w')
    dump(config, fichier)


def open_saved_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def write_json(data, output):
    with open(output, 'w') as f:
        json.dump(data, f)
