import os

from flask import Flask
from flask import render_template, send_from_directory

app = Flask(__name__, template_folder="./template/")

file_dir = "/home/hotaro/bessmertny_razmetka_7/"
entries_to_map = sorted([x[0].split("/")[-1] for x in os.walk(file_dir)])[1:]


def get_file(extension, path_to_dir):
    filenames = os.listdir(path_to_dir)
    return [path_to_dir + "/" + filename for filename in filenames if filename.endswith(extension)][0]


def read_line_from_path(path):
    file = open(path)
    line = file.read().replace("\n", " ")
    file.close()
    return line


@app.route('/')
def list():
    return render_template('list.html', count=len(entries_to_map), entries=entries_to_map)


@app.route('/file/<entry>/<file>')
def entry(entry, file):
    print(file)
    return send_from_directory(file_dir + entry, file) # lol vulnerability


@app.route('/<entry>')
def fentry(entry):
    entry_name = entry
    idx = entries_to_map.index(entry)
    count = len(entries_to_map)
    next_entry_idx = idx + 1
    if next_entry_idx >= len(entries_to_map):
        next_entry_idx = 0
    prev_entry_idx = idx - 1
    if prev_entry_idx < 0:
        prev_entry_idx = len(entries_to_map) - 1
    next_entry = entries_to_map[next_entry_idx]
    prev_entry = entries_to_map[prev_entry_idx]
    entry_root_dir = file_dir + entry
    try:
        text_filename = get_file("txt", entry_root_dir)
        text = read_line_from_path(text_filename)
    except Exception:
        text_filename = "<error>"
        text = "<error>"
    try:
        img_filename = "/file/" + entry + "/" + get_file("jpg", entry_root_dir).split("/")[-1]
    except Exception:
        img_filename = "<none>"

    text_request = ""
    split = text.split("\t")
    i = 1
    while i < len(split):
        split_entry = split[i]
        if split_entry.startswith("http"):
            break
        text_request += " " + split_entry
        i += 1
    return render_template('entry.html',
                           entry_name=entry_name,
                           idx=idx + 1,
                           count=count,
                           next_entry=next_entry,
                           prev_entry=prev_entry,
                           text_filename=text_filename,
                           text=text,
                           img_filename=img_filename,
                           request=text_request)


if __name__ == '__main__':
    app.run()
