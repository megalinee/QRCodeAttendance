import json
import shutil
import pandas as pd
import Constants as CONSTANT


def create_json(data, filename=CONSTANT.pathToJSON):
    f = open(filename, "w")
    f.write(data)
    f.close()


def read_json(filename=CONSTANT.pathToJSON):
    with open(filename,) as file:
        return json.load(file)


def write_json(new_data, filename=CONSTANT.pathToJSON):
    with open(filename, 'w') as file:
        file.seek(0)
        json.dump(new_data, file, indent=4)


def parse_nested_json(json_d):
    result = {}
    for key in json_d.keys():
        if not isinstance(json_d[key], dict):
            result[key] = json_d[key]
        else:
            result.update(parse_nested_json(json_d[key]))
    return result


def json_to_csv(json, path):
    json_data = pd.read_json(json)
    json_list = [j[1][0] for j in json_data.iterrows()]
    parsed_list = [parse_nested_json(j) for j in json_list]
    result = pd.DataFrame(parsed_list)
    result.to_csv(path, index=False, line_terminator='\n')


def duplicate_json(path):
    path.write(json.dumps(read_json()))
