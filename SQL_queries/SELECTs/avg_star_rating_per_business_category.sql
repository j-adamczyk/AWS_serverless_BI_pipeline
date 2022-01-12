SELECT AVG(stars) as "avg_category_rating", categories
FROM "yelp"."business"
GROUP BY categories;