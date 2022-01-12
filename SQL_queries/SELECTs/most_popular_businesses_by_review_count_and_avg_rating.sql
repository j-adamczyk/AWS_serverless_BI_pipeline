SELECT business_id, name, AVG(stars) AS "avg_rating", review_count
FROM "yelp"."business"
GROUP BY name, review_count, business_id
HAVING AVG(stars) > 4
ORDER BY review_count DESC;