CREATE DATABASE produce_aggregator;
use produce_aggregator;

CREATE TABLE farmers (
    farmer_id INT PRIMARY KEY,
    location VARCHAR(50),
    crop VARCHAR(50),
    avg_yield_kg INT,
    reliability_score DECIMAL(3,2)
);

CREATE TABLE daily_market_prices (
    date DATE,
    market VARCHAR(50),
    crop VARCHAR(50),
    price_per_kg DECIMAL(8,2),
    INDEX idx_date_crop (date, crop)
);

CREATE TABLE supply_records (
    farmer_id INT,
    date DATE,
    crop VARCHAR(50),
    quantity_available INT,
    INDEX idx_supply_date (date),
    FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
);

CREATE TABLE sales (
    date DATE,
    market VARCHAR(50),
    crop VARCHAR(50),
    quantity_sold INT,
    selling_price DECIMAL(8,2),
    INDEX idx_sales_date (date)
);
delete transport_costs from produce_aggregator;
CREATE TABLE transport_costs (
    route_id INT,
    origin_location VARCHAR(50),
    market VARCHAR(50),
    distance_km INT,
    cost_per_trip DECIMAL(10,2),
    capacity_kg INT
);


CREATE TABLE IF NOT EXISTS forecasts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    crop VARCHAR(50),
    market VARCHAR(50),
    model VARCHAR(20),
    forecast_value FLOAT
);



SHOW VARIABLES LIKE 'secure_file_priv';


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/farmers.csv'
INTO TABLE farmers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/daily_market_prices.csv'
INTO TABLE daily_market_prices
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/supply_records.csv'
INTO TABLE supply_records
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/transport_costs.csv'
INTO TABLE transport_costs
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT COUNT(*) FROM farmers;
SELECT COUNT(*) FROM daily_market_prices;
SELECT COUNT(*) FROM supply_records;
SELECT COUNT(*) FROM sales;
SELECT COUNT(*) FROM transport_costs;

SELECT * FROM farmers LIMIT 5;








-- 1
SELECT
    s.crop,
    s.market,
    SUM(
        (s.selling_price - p.price_per_kg) * s.quantity_sold
    ) AS net_profit
FROM sales s
JOIN daily_market_prices p
  ON s.date = p.date
 AND s.crop = p.crop
 AND s.market = p.market
GROUP BY s.crop, s.market
ORDER BY net_profit DESC;
-- 2
SELECT
    DATE_FORMAT(s.date, '%Y-%u') AS year_week,
    SUM((s.selling_price - p.price_per_kg) * s.quantity_sold) AS weekly_profit
FROM sales s
JOIN daily_market_prices p
  ON s.date = p.date
 AND s.crop = p.crop
 AND s.market = p.market
GROUP BY year_week
ORDER BY year_week;
-- 3
SELECT
    market,
    AVG(price_per_kg) / STDDEV(price_per_kg) AS risk_adjusted_return
FROM daily_market_prices
GROUP BY market
ORDER BY risk_adjusted_return DESC;
-- 4
SELECT
    crop,
    STDDEV(price_per_kg) AS price_volatility
FROM daily_market_prices
GROUP BY crop
ORDER BY price_volatility DESC;
-- 5
SELECT
    f.farmer_id,
    f.reliability_score,
    SUM(
        sr.quantity_available * p.price_per_kg * f.reliability_score
    ) AS weighted_value
FROM supply_records sr
JOIN farmers f ON sr.farmer_id = f.farmer_id
JOIN daily_market_prices p
  ON sr.date = p.date
 AND sr.crop = p.crop
GROUP BY f.farmer_id, f.reliability_score
ORDER BY weighted_value DESC;
-- 6
SELECT
    s.crop,
    s.market,
    AVG(s.selling_price - p.price_per_kg) AS avg_margin
FROM sales s
JOIN daily_market_prices p
  ON s.date = p.date
 AND s.crop = p.crop
 AND s.market = p.market
GROUP BY s.crop, s.market
HAVING avg_margin < 20
ORDER BY avg_margin;
-- 7
SELECT
    s.crop,
    AVG(
        s.selling_price
        - p.price_per_kg
        - (t.cost_per_trip / t.capacity_kg)
    ) AS margin_per_kg
FROM sales s
JOIN daily_market_prices p
  ON s.date = p.date
 AND s.crop = p.crop
 AND s.market = p.market
JOIN transport_costs t
  ON s.market = t.market
GROUP BY s.crop
ORDER BY margin_per_kg DESC;
-- 8
SELECT
    s.crop,
    s.market,
    SUM(
        GREATEST(s.quantity_sold - IFNULL(sr.quantity_available, 0), 0)
        * s.selling_price
    ) AS lost_revenue
FROM sales s
LEFT JOIN supply_records sr
  ON s.date = sr.date
 AND s.crop = sr.crop
GROUP BY s.crop, s.market
ORDER BY lost_revenue DESC;
-- 9
SELECT
    origin_location,
    market,
    cost_per_trip / capacity_kg AS cost_per_kg
FROM transport_costs
ORDER BY cost_per_kg DESC;
-- 10
SELECT
    crop,
    AVG(selling_price - price_per_kg) AS avg_margin
FROM sales s
JOIN daily_market_prices p
  ON s.date = p.date
 AND s.crop = p.crop
GROUP BY crop
ORDER BY avg_margin DESC;

-- 11
SELECT
    s.crop,
    SUM((s.selling_price - p.price_per_kg) * s.quantity_sold) AS profit
FROM sales s
JOIN daily_market_prices p
  ON s.date = p.date
 AND s.crop = p.crop
GROUP BY crop
ORDER BY profit DESC;
-- 12
SELECT crop, price_per_kg AS worst_case_price
FROM (
    SELECT 
        crop,
        price_per_kg,
        NTILE(10) OVER (PARTITION BY crop ORDER BY price_per_kg) AS percentile_group
    FROM daily_market_prices
) t
WHERE percentile_group = 1;
-- 13
SELECT
    market,
    SUM(capacity_kg) AS total_capacity
FROM transport_costs
GROUP BY market;
-- 14
SELECT
    s.crop,
    STDDEV(selling_price - price_per_kg) AS margin_volatility
FROM sales s
JOIN daily_market_prices p
  ON s.date = p.date
 AND s.crop = p.crop
GROUP BY crop
ORDER BY margin_volatility DESC;
-- 15
SELECT 
    s.crop,
    AVG((selling_price - price_per_kg) * quantity_sold) AS expected_profit
FROM sales s
JOIN daily_market_prices p
  ON s.date = p.date
 AND s.crop = p.crop
GROUP BY s.crop
ORDER BY expected_profit DESC;

-- 17
SELECT
    date,
    crop,
    market,
    price_per_kg AS price
FROM daily_market_prices;

-- 18
SELECT
    date,
    crop,
    market,
    SUM(quantity_sold) AS demand
FROM sales
GROUP BY date, crop, market
ORDER BY date;

-- 19
SELECT
    date,
    farmer_id,
    crop,
    SUM(quantity_available) AS supply
FROM supply_records
GROUP BY date, farmer_id, crop
ORDER BY date;

-- 20
SELECT
    origin_location,
    market,
    cost_per_trip,
    capacity_kg
FROM transport_costs;

-- 21
SELECT
    crop,
    market,
    COUNT(*) AS observations
FROM daily_market_prices
GROUP BY crop, market;

-- 22
SELECT 
    p.date,
    p.crop,
    p.market,
    p.price_per_kg AS actual_price,
    f.forecast_value
FROM prices p
LEFT JOIN forecasts f
ON p.date = f.date
AND p.crop = f.crop
AND p.market = f.market