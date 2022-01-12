SELECT b.business_id, b.review_count, count(user_id) as review_cnt_calculated, b.review_count = count(user_id) as valid
FROM "yelp"."business" as b LEFT JOIN "yelp"."review" as r ON b.business_id = r.business_id
GROUP BY b.business_id, b.review_count