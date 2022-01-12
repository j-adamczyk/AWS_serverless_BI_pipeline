SELECT state, AVG(stars) AS "avg_stars"
FROM "yelp"."business"
GROUP BY state
ORDER BY AVG(stars) DESC
LIMIT 10;