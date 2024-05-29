""" Logic behind bodyBinder"""

from config_manager import *

config = get_config('config.yml')

parsed_file = config['parsed_file']
output_file = config['output_file']
category_file = 'data/categories.json'


parsed = open_saved_json(parsed_file)
categories = open_saved_json(category_file)


def check_output_format(loaded_json):
    if loaded_json == {}:
        return {key: [] for key in categories['primary']}
    else:
        return loaded_json


output = open_saved_json(output_file)
output = check_output_format(output)


def get_remaining_labels():
    return parsed['to_tag']


def get_tagged_labels():
    return parsed['tagged']


def tag_label(index, category):
    global parsed, output
    label = parsed['to_tag'][index]
    output[category].append(label)
    parsed['to_tag'].pop(index)
    parsed['tagged'].append(label)


def untag_label(label, category):
    global parsed, output
    output[category].remove(label)
    parsed['to_tag'].append(label)
    parsed['tagged'].remove(label)


def display_cache():
    global parsed, output
    print(f'Parsed to tag : {parsed["to_tag"]}')
    print(f'Parsed tagged: {parsed["tagged"]}')
    print(f'Output : {output}')


def save_progress():
    write_json(parsed, parsed_file)
    write_json(output, output_file)


def get_catergories():
    return categories['primary']

