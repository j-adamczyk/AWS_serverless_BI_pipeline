# AWS Serverless BI Pipeline

A proof-of-concept (PoC) project for serverless Business Intelligence (BI) pipeline for non-relational data, using AWS tech stack:
- AWS S3 - data lake
- AWS Glue - data crawler (schema discovery tool)
- AWS Athena - SQL query engine
- AWS QuickSight - visualization tool

## Data processing scripts

A few scripts for processing the Yelp dataset. The code assumes that .json 
files are in the `/data` subdirectory, with raw JSONs (base dataset) in the 
`/data/raw_data`. Other subdirectories are created by scripts as needed.

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

Results are saved in `/data/cleaned_data`. They are in default Athena format, 
i.e. list of JSONs, one per line, separated with newlines.

### `json_to_tabular.py`

This scripts converts collections of JSONs, created with `clean_data.py`, to 
CSV or Apache Parquet. Results are saved in `/data/csv_data` or `/data/parquet_data`, 
depending on target format.


