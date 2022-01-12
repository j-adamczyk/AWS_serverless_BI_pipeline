SELECT city, AVG(stars) AS "avg_stars"
FROM "yelp"."business"
GROUP BY city
ORDER BY AVG(stars) DESC
LIMIT 10;