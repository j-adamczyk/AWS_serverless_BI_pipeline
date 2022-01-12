CREATE OR REPLACE VIEW ten_most_active_cities AS

SELECT city, SUM(review_count) AS total_review_count
FROM "yelp"."business" AS business
GROUP BY city
ORDER BY SUM(review_count) DESC
LIMIT 10;