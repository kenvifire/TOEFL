import os
import json
import re
import platform
import shutil

def read_score(file_path):
    current_file = open(file_path, 'r')
    lines = current_file.readlines()
    score = 0

    if platform.system() == 'Windows':
        date = os.path.getctime(file_path)
    else:
        stat = os.stat(file_path)
        try:
            date = stat.st_birthtime
        except AttributeError:
            date = stat.st_mtime


    regx = r"[Ss]core\s+(\d+)"
    for line in lines:
        matches = re.search(regx, line)
        if matches:
            score = matches.group(1)
            break

    index_regx = r"(\d+)"
    matches = re.search(index_regx, file_path)
    if matches:
        index = matches.group(1)

    return index, date*1000, score

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
                'type': dir,
            })
    return list

def generate_data(work_dir, build_dir):
    result = []
    for dir in ['reading', 'listening']:

        data = read_dir(os.path.join(work_dir, dir))
        result += data

    json_content = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
    build_file = open(os.path.join(build_dir, "score.json"), 'w')
    build_file.write(json_content)
    build_file.close()


if __name__ == "__main__":
    build_dir = './build/english/toefl/'
    shutil.rmtree("./build", ignore_errors=True)
    os.makedirs(build_dir)
    generate_data('.', build_dir)



