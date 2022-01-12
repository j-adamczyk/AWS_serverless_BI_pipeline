select user_id, review_count
from "yelp"."user"
order by review_count desc
limit 1