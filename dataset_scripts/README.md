# Dataset cleaning scripts

A few scripts for processing the Yelp dataset. The code assumes that .json 
files are in the `/data` subdirectory, with raw JSONs (base dataset) in the 
`/data/raw_data`. Other subdirectories are created by scripts as needed.

### `reduce_data.py`

This script reduces the Yelp dataset to a subset used for further analysis:
- `yelp_academic_dataset_business.json`:
  - reformatting due to inconsistencies of data, e.g. change `u'"value"'` to `"value"`
  - change `categories` ` from comma-separated string to list
  - change `hours` to `days_open`: drop hours information, use only days of week
  - drop `address`, `postal_code` and `is_open`
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

Results are saved in `/data/cleaned_data`.
  