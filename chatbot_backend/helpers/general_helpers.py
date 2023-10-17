import json
import os


def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def load_config(config_filepath):
    with open(config_filepath) as config_file:
        return json.load(config_file)


def write_to_txt_file(filepath, content):
    make_folder(filepath.parent)
    with open(filepath, "w") as file:
        file.write(content)


def read_txt_file(filepath):
    with open(filepath, "r") as file:
        return file.read()


def system_msg(msg):
    return f"\n=== [{msg}] ==="
