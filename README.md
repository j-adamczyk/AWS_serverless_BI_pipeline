# AWS Serverless BI Pipeline

A proof-of-concept (PoC) project for serverless Business Intelligence (BI) pipeline for non-relational data, using AWS tech stack:
- AWS S3 - data lake
- AWS Glue - data crawler (schema discovery tool)
- AWS Athena - SQL query engine
- AWS QuickSight - visualization tool

## Data preprocessing scripts

A few scripts in `data_preprocessing_scripts` directory for cleaning and preprocessing the Yelp dataset. 

The code assumes the following directories structure:
- `/data_preprocessing_scripts/data/raw_data` - contain raw `business.json`, `review.json` and `user.json` from the Yelp dataset
- `/data_preprocessing_scripts/data` - contain (empty) `csv_data`, `json_data`, `json_data_schemas` and `parquet_data` directories

### `clean_data.py`

This script performs the initial cleaning of the Yelp dataset before further analysis:
- `yelp_academic_dataset_business.json`:
  - reformatting due to inconsistencies of data, e.g. change `u'"value"'` to `"value"`
  - change `categories` ` from comma-separated string to list
  - change `hours` to `days_open`: drop hours information, use only days of week
  - drop `address`, `postal_code` and `is_open`
  - heavy changes to `attributes` - selection of only a few, make data types more consistent
- `yelp_academic_dataset_checkin.json`:
  - dropped, will not be used
- `yelp_academic_dataset_review.json`:
  - drop review text
  - drop `review_id`
  - drop `date` time information, use hour only
- `yelp_academic_dataset_tip.json`:
  - dropped, will not be used
- `yelp_academic_dataset_user.json`:
  - drop `friends` and `name`
  - drop `yelping_since` time information, use hour only
  - change `elite` from comma-separated string to list

Results are saved in `/data/json_data`. They are in default Athena format, 
i.e. JSON stream (list of JSONs, one per line, separated with newlines).

### `discover_schemas.py`

This script crawls cleaned JSONs from `/data/json_data` and saves their schemas 
in `/data/json_data_schemas`. This is done to:
- explore the schemas 
- debugging data cleaning script, avoiding paying for AWS Glue Crawler just 
  to discover a bug
- validate data types discovered by Glue

### `json_to_tabular.py`

This script converts collections of JSONs, created with `clean_data.py`, to 
CSV or Apache Parquet. Results are saved in `/data/csv_data` or `/data/parquet_data`, 
depending on target format.

## Athena SQL queries

SQL queries for usage in AWS Athena for benchmarking the approaches are in `SQL_queries` directory.
