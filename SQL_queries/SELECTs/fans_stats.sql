select avg(fans) as avg, min(fans) as min, max(fans) as max, approx_percentile(fans,0.5) as median
from "yelp"."user"