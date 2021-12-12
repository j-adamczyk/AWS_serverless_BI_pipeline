import json
import os

from genson import SchemaBuilder

DATA_DIR = os.path.join("data", "cleaned_data")


def print_schema(filename: str) -> None:
    with open(os.path.join(DATA_DIR, filename)) as file:
        schema_builder = SchemaBuilder()
        schema_builder.add_object(json.load(file))
        schema = schema_builder.to_json(indent=2)
        print(schema)


if __name__ == '__main__':
    print("Business schema:")
    print_schema("business.json")
    print()

    print("Review schema:")
    print_schema("review.json")
    print()

    print("User schema:")
    print_schema("user.json")
