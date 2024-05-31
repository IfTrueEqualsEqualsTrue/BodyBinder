""" Logic behind bodyBinder"""

from config_manager import *
import subprocess
import os

config = get_config('config.yml')

if not config['parsed_file']:
    parsed_file = 'data/ressources/dummy.json'
else:
    parsed_file = config['parsed_file']
output_file = 'data/output/output.json'
category_file = 'data/output/categories.json'


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


class TagManager:

    def __init__(self):
        self.complete = False
        self.index = len(parsed['tagged']) if len(parsed['tagged']) != 0 else 1
        self.total_tag = len(parsed['to_tag']) + len(parsed['tagged'])

    def next(self, category):
        tag_label(0, category)
        if self.index < self.total_tag - 1:
            self.index += 1
            if self.index % 5 == 0:
                save_progress()
        else:
            self._end()
            return self.total_tag, 'end'
        return self.index - 1, parsed['to_tag'][0]

    def _end(self):
        self.complete = True
        save_progress()

    def get_current_name(self):
        try:
            return parsed['to_tag'][self.index - 1]
        except IndexError:
            return 'Terminé !'


def change_parsed_file(new_file):
    global parsed, config, parsed_file
    parsed_file = new_file
    parsed = open_saved_json(new_file)
    config['parsed_file'] = new_file
    save_config(config, 'config.yml')


def get_tagger():
    return TagManager()


def open_output():
    subprocess.Popen(f'explorer /select,"{os.path.join(os.getcwd(), "data\output", "output.json")}"')

