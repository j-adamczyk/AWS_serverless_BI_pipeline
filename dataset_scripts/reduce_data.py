from collections import Counter
import json
import os
import re
from typing import Any, Callable, Dict

from tqdm import tqdm


IN_DATA_DIR = os.path.join("data", "raw_data")
OUT_DATA_DIR = os.path.join("data", "cleaned_data")

JsonType = Dict[str, Any]


def get_num_lines(filepath: str) -> int:
    with open(filepath, encoding="UTF-8") as file:
        num_lines = 0
        for _ in file:
            num_lines += 1

        return num_lines


def process_file(
    in_filename: str, out_filename: str, single_json_fun: Callable[[JsonType], JsonType]
) -> None:
    in_filepath = os.path.join(IN_DATA_DIR, in_filename)
    out_filepath = os.path.join(OUT_DATA_DIR, out_filename)

    if os.path.exists(out_filepath):
        os.remove(out_filepath)

    with open(in_filepath, encoding="UTF-8") as in_file, open(
        out_filepath, "w", encoding="UTF-8"
    ) as out_file:
        lines = []
        for line in tqdm(in_file, total=get_num_lines(in_filepath)):
            processed_line = single_json_fun(json.loads(line))
            lines.append(processed_line)

        json.dump(lines, out_file, sort_keys=True, default=str)


def business_json_fun(line_json: JsonType) -> JsonType:
    string_json = (
        json.dumps(line_json)
        .replace('"True"', "true")
        .replace('"False"', "false")
    )
    string_json = re.sub(r"u'([\s\S]+?)'", r"\1", string_json)
    string_json = re.sub(r"\"'([\s\S]+?)'\"", r'"\1"', string_json)

    line_json = json.loads(string_json)

    try:
        categories = line_json["categories"].split(",")
        line_json["categories"] = list(map(str.strip, categories))
    except AttributeError:
        pass

    try:
        line_json["days_open"] = list(line_json["hours"].keys())
        del line_json["hours"]
    except AttributeError:
        pass

    del line_json["address"]
    del line_json["postal_code"]
    del line_json["is_open"]

    result = line_json
    return result


def checkin_json_fun(line_json: JsonType) -> JsonType:
    line_json["date"] = Counter(
        date_time.split()[0] for date_time in line_json["date"].split(", ")
    )
    return line_json


def review_json_fun(line_json: JsonType) -> JsonType:
    del line_json["review_id"]
    del line_json["text"]
    line_json["date"] = line_json["date"].split()[0]  # select date only

    return line_json


def tip_json_fun(line_json: JsonType) -> JsonType:
    line_json["date"] = line_json["date"].split()[0]
    del line_json["text"]
    return line_json


def user_json_fun(line_json: JsonType) -> JsonType:
    del line_json["friends"]
    del line_json["name"]

    line_json["yelping_since"] = line_json["yelping_since"].split()[0]

    try:
        elite_years = line_json["elite"].split(",")
        line_json["elite"] = list(map(int, elite_years))
    except AttributeError:
        pass

    return line_json


if __name__ == "__main__":
    for in_filename, out_filename, single_line_fun in [
        ("yelp_academic_dataset_business.json", "business.json", business_json_fun),
        ("yelp_academic_dataset_review.json", "review.json", review_json_fun),
        ("yelp_academic_dataset_user.json", "user.json", user_json_fun),
    ]:
        print(f"{out_filename} starting")
        process_file(in_filename, out_filename, single_line_fun)
        print()
