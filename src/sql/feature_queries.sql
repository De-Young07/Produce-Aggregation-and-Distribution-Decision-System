-- Base market dataset

CREATE OR REPLACE VIEW market_daily_features AS

SELECT
    p.date,
    p.crop,
    p.market,
    p.price_per_kg,
    d.demand,
    SUM(s.quantity_supplied) AS total_supply

FROM prices p

JOIN demand d
ON p.date = d.date
AND p.crop = d.crop
AND p.market = d.market

LEFT JOIN supply s
ON p.crop = s.crop
AND p.date = s.date

GROUP BY
p.date,
p.crop,
p.market,
p.price_per_kg,
d.demand;



-- Extended feature dataset

CREATE OR REPLACE VIEW market_features_extended AS

SELECT

date,
crop,
market,
price_per_kg,
demand,
total_supply,

AVG(price_per_kg)
OVER(
PARTITION BY crop, market
ORDER BY date
ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
) AS price_ma7,

AVG(price_per_kg)
OVER(
PARTITION BY crop, market
ORDER BY date
ROWS BETWEEN 30 PRECEDING AND CURRENT ROW
) AS price_ma30

FROM market_daily_features;