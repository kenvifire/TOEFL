import os
import json
import re
import shutil
import time
import datetime


def read_score(file_path):
    current_file = open(file_path, 'r')
    lines = current_file.readlines()
    score = 0

    regx = r"[Ss]core\s+(\d+)"
    for line in lines:
        matches = re.search(regx, line)
        if matches:
            score = matches.group(1)
            break

    date_regx = r"[Dd]ate (\d{4}\-\d{2}\-\d{2})"
    for line in lines:
        matches = re.search(date_regx, line)
        if matches:
            date = time.mktime(datetime.datetime.strptime(matches.group(1), "%Y-%m-%d").timetuple())
            date = int(date * 1000)
            break

    index_regx = r"(\d+)"
    matches = re.search(index_regx, file_path)
    if matches:
        index = matches.group(1)

    return index, date, score

def read_dir(dir):
    list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            index, date, score = read_score(os.path.join(root, file))
            list.append({
                'index': index,
                'date': date,
                'file': file,
                'score': score,
                'type': dir[2:],
            })
    return list


def generate_data(work_dir, build_dir):
    data_list = []
    progress_list = []
    for dir in ['reading', 'listening']:
        data = read_dir(os.path.join(work_dir, dir))
        progress_list.append({'type': dir, 'percent': len(data) * 100/58.0})

        data_list += data

    for dir in ['writing', 'speaking']:
        progress_list.append({'type': dir, 'percent': 0 * 100/58.0})

    files = next(os.walk(os.path.join(work_dir, 'words')))[2]
    word_cnt = len(files)
    progress_list.append({'type': 'words', 'percent': word_cnt * 100 / 94.0})

    result = {}
    result['data'] = data_list
    result['progress'] = progress_list

    json_content = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
    build_file = open(os.path.join(build_dir, "score.json"), 'w')
    build_file.write(json_content)
    build_file.close()


if __name__ == "__main__":
    build_dir = './build/english/toefl/'
    shutil.rmtree("./build", ignore_errors=True)
    os.makedirs(build_dir)
    generate_data('.', build_dir)
