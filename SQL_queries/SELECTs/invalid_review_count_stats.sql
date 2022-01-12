SELECT count(business_id) as nequal_count, cast(count(business_id) as decimal(10,2))/cast((select count(*) from "yelp"."business") as decimal(10,2))*100 as nequal_percent
FROM (select b.business_id, b.review_count, count(user_id)
        FROM "yelp"."business" as b LEFT JOIN "yelp"."review" as r ON b.business_id = r.business_id
        GROUP BY b.business_id, b.review_count
        HAVING b.review_count != count(user_id))