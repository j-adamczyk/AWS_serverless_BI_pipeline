from collections import Counter
import copy
import json
import os
from typing import Any, Callable, Dict

import regex as re
from tqdm import tqdm


IN_DATA_DIR = os.path.join("data", "raw_data")
OUT_DATA_DIR = os.path.join("data", "json_data")

JsonType = Dict[str, Any]


def get_num_lines(filepath: str) -> int:
    with open(filepath, encoding="UTF-8") as file:
        num_lines = 0
        for _ in file:
            num_lines += 1

        return num_lines


def process_attributes(attributes: Dict[str, Any]) -> Dict[str, Any]:
    attributes = copy.deepcopy(attributes)

    for attr_name, fill_value in [
        ("AcceptsInsurance", False),
        ("Alcohol", "none"),
        ("BikeParking", False),
        ("BusinessAcceptsBitcoin", False),
        ("BusinessAcceptsCreditCards", False),
        ("ByAppointmentOnly", False),
        ("BYOB", False),
        ("Caters", False),
        ("CoatCheck", False),
        ("Corkage", False),
        ("DogsAllowed", False),
        ("DriveThru", False),
        ("GoodForDancing", False),
        ("GoodForKids", False),
        ("HappyHour", False),
        ("HasTV", False),
        ("NoiseLevel", "average"),
        ("Open24Hours", False),
        ("OutdoorSeating", False),
        ("RestaurantsAttire", "casual"),
        ("RestaurantsDelivery", False),
        ("RestaurantsCounterService", False),
        ("RestaurantsGoodForGroups", False),
        ("RestaurantsReservations", True),
        ("RestaurantsTableService", True),
        ("RestaurantsTakeOut", False),
        ("Smoking", "no"),
        ("WiFi", "no"),
        ("WheelchairAccessible", False),
    ]:
        attr_value = attributes.get(attr_name, None)
        attr_value = fill_value if attr_value is None else attr_value
        attributes[attr_name] = attr_value

    for attr_name, fill_value in [
        ("Ambience", False),
        ("BusinessParking", False),
        ("GoodForMeal", False),
        ("Music", False),
    ]:
        attr_value = attributes.get(attr_name, None)
        if attr_value is not None:
            attr_value = {
                key: (fill_value if val is None else val)
                for key, val in attr_value.items()
            }
            attributes[attr_name] = attr_value
        else:
            attributes[attr_name] = None

    if "RestaurantsPriceRange2" in attributes:
        attr_name = "RestaurantsPriceRange"

        attr_value = attributes["RestaurantsPriceRange2"]
        attr_value = 3 if attr_value is None else int(attr_value)

        attributes[attr_name] = attr_value
        del attributes["RestaurantsPriceRange2"]

    for attr_name in ["HairSpecializesIn", "BestNights", "BYOBCorkage"]:
        if attr_name in attributes:
            del attributes[attr_name]

    attr_name = "AgesAllowed"
    attr_value = attributes.get(attr_name, "allages")
    if attr_value.startswith("u'"):
        # cases like "u'18plus'" value
        attr_value = attr_value[2:-1]
    attributes[attr_name] = attr_value

    return attributes


def process_file(
    in_filename: str, out_filename: str, single_json_fun: Callable[[JsonType], JsonType]
) -> None:
    in_filepath = os.path.join(IN_DATA_DIR, in_filename)
    out_filepath = os.path.join(OUT_DATA_DIR, out_filename)

    if os.path.exists(out_filepath):
        os.remove(out_filepath)

    with open(in_filepath, encoding="utf-8") as in_file, open(
        out_filepath, "w", encoding="utf-8"
    ) as out_file:
        for line in tqdm(in_file, total=get_num_lines(in_filepath)):
            processed_line = single_json_fun(json.loads(line))
            line_string = json.dumps(processed_line, sort_keys=True, default=str)
            line_string = f"{line_string}\n"
            out_file.write(line_string)


def business_json_fun(line_json: JsonType) -> JsonType:
    string_json = (
        json.dumps(line_json)
        .replace('"True"', "true")
        .replace('"False"', "false")
        .replace("True", "true")
        .replace("False", "false")
        .replace('"{', "{")
        .replace('}"', "}")
    )
    string_json = re.sub(r"u'([a-zA-Z_]+?)'", r"\1", string_json)
    string_json = re.sub(r"\"'([\s\S]+?)'\"", r'"\1"', string_json)
    string_json = re.sub(r"'([a-zA-Z_\-]+?)':", r'"\1":', string_json)
    string_json = re.sub(r'{([a-zA-Z]+)"', r'{"\1"', string_json)
    string_json = re.sub("'([a-zA-Z]+)\":", r'"\1":', string_json)

    string_json = string_json.replace("None", "null")
    string_json = string_json.replace('"null"', "null")
    string_json = string_json.replace("{'", '{"')

    line_json = json.loads(string_json)

    try:
        categories = line_json["categories"].split(",")
        line_json["categories"] = list(map(str.strip, categories))
    except AttributeError:
        line_json["categories"] = None

    try:
        attributes = line_json["attributes"]
        if attributes is not None:
            line_json["attributes"] = process_attributes(attributes)
    except AttributeError:
        line_json["attributes"] = None

    try:
        line_json["days_open"] = list(line_json["hours"].keys())
    except AttributeError:
        line_json["days_open"] = None

    del line_json["hours"]
    del line_json["address"]
    del line_json["postal_code"]
    del line_json["is_open"]

    return line_json


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

    elite_years = line_json["elite"]
    if elite_years:
        line_json["elite"] = list(map(int, elite_years.split(",")))
    else:
        line_json["elite"] = []

    return line_json


if __name__ == "__main__":
    for in_filename, out_filename, single_line_fun in [
        ("yelp_academic_dataset_business.json", "business", business_json_fun),
        ("yelp_academic_dataset_review.json", "review", review_json_fun),
        ("yelp_academic_dataset_user.json", "user", user_json_fun),
    ]:
        print(f"{out_filename} starting")
        process_file(in_filename, out_filename, single_line_fun)
        print()
