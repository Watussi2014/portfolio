--- Views that return analytical data for today, yesterday, the current week and the last seven days.

CREATE VIEW analytics_today AS
SELECT  city,
		MAX(temp) max_temp,
		MIN(temp) min_temp,
		stddev(temp) std_deviation
FROM weather_data
WHERE date(timestamp) = current_date
GROUP BY city
;

CREATE VIEW analytics_yesterday AS
SELECT  city,
		MAX(temp) max_temp,
		MIN(temp) min_temp,
		stddev(temp) std_deviation
FROM weather_data
WHERE date(timestamp) = current_date - 1
GROUP BY city
;

CREATE VIEW analytics_current_week AS
SELECT  city,
		MAX(temp) max_temp,
		MIN(temp) min_temp,
		stddev(temp) std_deviation
FROM weather_data
WHERE date_trunc('week',timestamp) = date_trunc('week',current_date)
GROUP BY city
;

CREATE VIEW analytics_last_seven AS
SELECT  city,
		MAX(temp) max_temp,
		MIN(temp) min_temp,
		stddev(temp) std_deviation
FROM weather_data
WHERE date(timestamp) >= current_date - 7
GROUP BY city
;