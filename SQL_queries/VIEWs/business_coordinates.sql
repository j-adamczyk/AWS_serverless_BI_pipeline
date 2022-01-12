CREATE OR REPLACE VIEW businesses_coordinates AS

SELECT latitude, longitude
FROM "yelp"."business";
