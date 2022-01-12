CREATE OR REPLACE VIEW business_rating_vs_popularity AS

SELECT b.business_id, b.stars, count(user_id) as reviews_cnt
FROM "yelp"."business" as b LEFT JOIN "yelp"."review" as r ON b.business_id = r.business_id
GROUP BY b.business_id, b.stars