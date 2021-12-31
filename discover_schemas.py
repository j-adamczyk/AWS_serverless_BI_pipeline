import json
import os
from typing import Optional

from genson import SchemaBuilder

DATA_DIR = os.path.join("data", "cleaned_data")
SCHEMAS_DIR = os.path.join("data", "cleaned_data_schemas")


def discover_schema(
    json_file_name: str, schema_file_name: Optional[str] = None
) -> None:
    """
    Discovers the schema of JSON collection and prints it (if schema_file is None),
    or saves it to schema_file (if not None).
    """
    with open(os.path.join(DATA_DIR, json_file_name)) as file:
        schema_builder = SchemaBuilder()

        for line in file:
            schema_builder.add_object(json.loads(line))

        schema = schema_builder.to_json(indent=2)

        if schema_file_name is None:
            print(schema)
        else:
            with open(schema_file_name, "w") as schema_file:
                schema_file.write(schema)

            print("Schema saved to", schema_file_name)


if __name__ == "__main__":
    print("Business schema:")
    filename = os.path.join(SCHEMAS_DIR, "business.json")
    discover_schema("business", filename)
    print()

    print("Review schema:")
    filename = os.path.join(SCHEMAS_DIR, "review.json")
    discover_schema("review", filename)
    print()

    print("User schema:")
    filename = os.path.join(SCHEMAS_DIR, "user.json")
    discover_schema("user", filename)
