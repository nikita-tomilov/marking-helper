import os

from flask import Flask, redirect
from flask import render_template, send_from_directory

app = Flask(__name__, template_folder="./template/")

if 'DATASET_FOLDER' not in os.environ:
    print('Set DATASET_FOLDER environment variable')
    exit(1)

file_dir = os.environ['DATASET_FOLDER']
if not file_dir.endswith('/'):
    file_dir += '/'

entries_to_map = sorted([x[0].split("/")[-1] for x in os.walk(file_dir)])[1:]


def get_file(extension, path_to_dir):
    filenames = os.listdir(path_to_dir)
    return [path_to_dir + "/" + filename for filename in filenames if filename.endswith(extension)][0]


def read_line_from_path(path):
    file = open(path, 'r', encoding='utf8')
    line = file.read().replace("\n", " ")
    file.close()
    return line


def write_line_to_path(path, line):
    file = open(path, "w", encoding='utf-8')
    file.write(line + "\n")
    file.close()


def write_mark_to_file(path, mark):
    line = read_line_from_path(path)
    split = line.split("\t")
    join = "\t".join(split[:-1])
    join = join + "\t" + mark
    print(join)
    write_line_to_path(path, join)


def check_if_done(entry):
    entry_root_dir = file_dir + entry
    try:
        text_filename = get_file("txt", entry_root_dir)
        text = read_line_from_path(text_filename).split("\t")[-1]
    except Exception:
        return ""
    text = text.strip()
    if len(text) == 0:
        return ""
    return "Marked as '" + text + "'"


@app.route('/')
def list():
    entries_with_marks = []
    done_count = 0
    for entry in entries_to_map:
        is_done = check_if_done(entry)
        entry_data = {"name": entry, "is_done": is_done}
        if len(is_done) > 0:
            done_count += 1
        entries_with_marks.append(entry_data)

    return render_template('list.html', count=len(entries_with_marks), entries=entries_with_marks, done_count=done_count)


@app.route('/file/<entry>/<file>')
def entry(entry, file):
    print(file)
    return send_from_directory(file_dir + entry, file) # lol vulnerability


@app.route('/mark/<entry>/<txtfile>/<marking>')
def markentry(entry, txtfile, marking):
    if not (marking.startswith("<")):
        print(entry, txtfile, marking)
        write_mark_to_file(file_dir + entry + "/" + txtfile, marking)

    idx = entries_to_map.index(entry)
    count = len(entries_to_map)
    next_entry_idx = idx + 1
    if next_entry_idx >= len(entries_to_map):
        next_entry_idx = 0
    next_entry = entries_to_map[next_entry_idx]

    return redirect("/" + str(next_entry), code=302)


@app.route('/<entry>')
def fentry(entry):
    if entry.startswith("<"):
        return "wtf"
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
        img_filename = None

    text_request = ""
    url = "<not found>"
    split = text.split("\t")
    i = 1
    while i < len(split):
        split_entry = split[i]
        if split_entry.startswith("http"):
            url = split_entry
            break
        text_request += " " + split_entry
        i += 1
    mark = split[-1]
    if not mark:
        mark = "<not set yet>"
    set_mark_neg = "/mark/" + entry + "/" + text_filename.split("/")[-1] + "/-1"
    set_mark_zero = "/mark/" + entry + "/" + text_filename.split("/")[-1] + "/0"
    set_mark_pos = "/mark/" + entry + "/" + text_filename.split("/")[-1] + "/1"
    return render_template('entry.html',
                           entry_name=entry_name,
                           idx=idx + 1,
                           count=count,
                           next_entry=next_entry,
                           prev_entry=prev_entry,
                           text_filename=text_filename,
                           text=text,
                           img_filename=img_filename,
                           request=text_request,
                           url=url,
                           mark=mark,
                           set_mark_neg=set_mark_neg,
                           set_mark_zero=set_mark_zero,
                           set_mark_pos=set_mark_pos)


if __name__ == '__main__':
    app.run()
