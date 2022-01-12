CREATE OR REPLACE VIEW average_star_rating_per_state AS
SELECT AVG(stars) as "average state rating", state FROM "yelp"."business" GROUP BY state;