BEGIN;

-- Initilizing the table with all the analytical data
CREATE TABLE IF NOT EXISTS public.price_table(
    "timestamp" TIMESTAMP WITH TIME ZONE NOT NULL,
    ticker VARCHAR(8) NOT NULL,
    name VARCHAR(15) NOT NULL,
    price_usd NUMERIC(9, 4) NOT NULL,
    PRIMARY KEY ("timestamp", ticker)
);

-- Initilizing the view that return the last 12 price for each metal in the database
CREATE OR REPLACE VIEW last_12_price AS (
WITH t1 as (
SELECT timestamp, ticker, name, price_usd,
rank() over (partition by ticker order by timestamp desc) as rank_time
from price_table)
SELECT 
ticker, price_usd
FROM t1
WHERE rank_time <= 12
ORDER BY timestamp DESC);

-- Initilizing the trigger that will send a signal to pull the data into the model pipeline
CREATE OR REPLACE FUNCTION notify_table_change() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('table_change', '');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER table_change_trigger
AFTER INSERT ON price_table
FOR EACH STATEMENT EXECUTE FUNCTION notify_table_change();

COMMIT;