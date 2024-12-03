-- Views that will return the max and min temp and the city associated for each hour, day and week

CREATE VIEW hourly_max_min AS
WITH temp_rank AS
(SELECT date_trunc('hours', timestamp) as hours,
		city,
		temp,
		RANK() OVER (PARTITION BY date_trunc('hours', timestamp) ORDER BY temp DESC) max_rank,
		RANK() OVER (PARTITION BY date_trunc('hours', timestamp) ORDER BY temp ASC) min_rank
FROM weather_data
)

SELECT hours,
		MAX(CASE WHEN max_rank = 1 THEN city END) AS max_temp_city,
		MAX(CASE WHEN max_rank = 1 THEN temp END) AS max_temp,
		MAX(CASE WHEN min_rank = 1 THEN city END) AS min_temp_city,
		MAX(CASE WHEN min_rank = 1 THEN temp END) AS min_temp
FROM temp_rank
GROUP BY hours
ORDER BY hours DESC



CREATE VIEW daily_max_min AS
WITH temp_rank AS
(SELECT date_trunc('day', timestamp) as days,
		city,
		temp,
		RANK() OVER (PARTITION BY date_trunc('day', timestamp) ORDER BY temp DESC) max_rank,
		RANK() OVER (PARTITION BY date_trunc('day', timestamp) ORDER BY temp ASC) min_rank
FROM weather_data
)

SELECT days,
		MAX(CASE WHEN max_rank = 1 THEN city END) AS max_temp_city,
		MAX(CASE WHEN max_rank = 1 THEN temp END) AS max_temp,
		MAX(CASE WHEN min_rank = 1 THEN city END) AS min_temp_city,
		MAX(CASE WHEN min_rank = 1 THEN temp END) AS min_temp
FROM temp_rank
GROUP BY days
ORDER BY days DESC


CREATE VIEW weekly_max_min AS
WITH temp_rank AS
(SELECT date_trunc('week', timestamp) as weeks,
		city,
		temp,
		RANK() OVER (PARTITION BY date_trunc('week', timestamp) ORDER BY temp DESC) max_rank,
		RANK() OVER (PARTITION BY date_trunc('week', timestamp) ORDER BY temp ASC) min_rank
FROM weather_data
)

SELECT weeks,
		MAX(CASE WHEN max_rank = 1 THEN city END) AS max_temp_city,
		MAX(CASE WHEN max_rank = 1 THEN temp END) AS max_temp,
		MAX(CASE WHEN min_rank = 1 THEN city END) AS min_temp_city,
		MAX(CASE WHEN min_rank = 1 THEN temp END) AS min_temp
FROM temp_rank
GROUP BY weeks
ORDER BY weeks DESC

