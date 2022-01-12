SELECT b.business_id, count(user_id) as reviews_cnt
FROM "yelp"."business" as b LEFT JOIN "yelp"."review" as r ON b.business_id = r.business_id
GROUP BY b.business_id
order by reviews_cnt DESC
limit 1