-- Views that return total hours of rains for all the city yesterday and last week

CREATE VIEW hours_rain_ytd AS
SELECT count(precip) as hours_of_rain_total
FROM weather_data
WHERE precip > 0
AND date(timestamp) = current_date - 1;

CREATE VIEW hours_rain_lastwk AS
SELECT count(precip) as hours_of_rain_total
FROM weather_data
WHERE precip > 0
AND date_trunc('week',timestamp) = date_trunc('week',current_date);