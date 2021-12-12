import json
import os


DATA_DIR = os.path.join("data", "cleaned_data")


def print_schema(filename: str) -> None:
    with open(os.path.join(DATA_DIR, filename)) as file:
        first_json = json.load(file)[0]

    print(json.dumps(first_json, indent=2))


if __name__ == '__main__':
    print_schema("business.json")
    print()
    print_schema("review.json")
    print()
    print_schema("user.json")
