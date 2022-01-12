SELECT stars, count(*)
from "yelp"."review"
group by stars