import csv
import json
import os
from typing import Any, Dict

import pandas as pd


DATA_DIR = os.path.join("data", "cleaned_data")
CSV_DATA_DIR = os.path.join("data", "csv_data")
PARQUET_DATA_DIR = os.path.join("data", "parquet_data")

JsonType = Dict[str, Any]


def jsons_file_to_tabular_file(in_filename: str, out_filename: str, target_format: str) -> None:
    assert target_format in {"csv", "parquet"}

    in_filepath = os.path.join(DATA_DIR, in_filename)
    df = pd.read_json(in_filepath, lines=True)

    # change single quotes ' to double quotes " in JSONs
    for col, dtype in zip(df.columns, df.dtypes):
        if dtype == "object":
            df[col] = (
                df[col]
                .astype(str).str
                .replace("'", '"')
                .replace("True", "true")
                .replace("False", "false")
                .replace("None", "null")
            )

    if target_format == "csv":
        out_filepath = os.path.join(CSV_DATA_DIR, out_filename)
        df.to_csv(out_filepath, index=False, sep=";", quoting=csv.QUOTE_NONE, escapechar="\\")
    else:
        out_filepath = os.path.join(PARQUET_DATA_DIR, out_filename)
        df.to_parquet(out_filepath, engine="pyarrow", compression="snappy", index=None)


if __name__ == '__main__':
    for in_filename in ["business", "review", "user"]:
        out_filename = f"{in_filename}.csv"
        #print(f"{out_filename} starting")
        #jsons_file_to_tabular_file(in_filename, out_filename, "csv")
        print()

        out_filename = f"{in_filename}.parquet"
        print(f"{out_filename} starting")
        jsons_file_to_tabular_file(in_filename, out_filename, "parquet")
        print()

