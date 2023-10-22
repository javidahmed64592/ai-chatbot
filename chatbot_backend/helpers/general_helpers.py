import json
import os


def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def load_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


def write_to_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file)


def update_json_file(filepath, updated_values):
    data = load_json(filepath)

    for key, value in updated_values.items():
        data[key] = value

    write_to_json(filepath, data)


def write_to_txt_file(filepath, content):
    make_folder(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


def read_txt_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def system_msg(msg):
    return f"\n=== [{msg}] ==="
