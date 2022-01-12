SELECT SUBSTR(r.date, 1, 4) as ryear, avg(r.stars) as average_stars
FROM "yelp"."business" as b INNER JOIN "yelp"."review" as r on b.business_id = r.business_id
WHERE b.business_id = (
    SELECT b.business_id
    FROM "yelp"."business" as b LEFT JOIN "yelp"."review" as r ON b.business_id = r.business_id
    GROUP BY b.business_id
    order by count(user_id) DESC
    limit 1
)
group by SUBSTR(r.date, 1, 4)
order by ryear

