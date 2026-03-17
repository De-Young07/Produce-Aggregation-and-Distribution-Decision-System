import numpy as np
import pandas as pd
from datetime import timedelta
import random

np.random.seed(42)

# -----------------------------
# PARAMETERS
# -----------------------------
START_DATE = "2023-01-01"
END_DATE = "2024-12-31"

CROPS = ["maize", "rice", "tomato"]
MARKETS = ["lagos", "ibadan", "abuja", "minna"]
LOCATIONS = ["northcentral", "southwest"]

N_FARMERS = 25

# -----------------------------
# DATE RANGE
# -----------------------------
dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")

# -----------------------------
# FARMERS
# -----------------------------
farmers = pd.DataFrame({
    "farmer_id": range(1, N_FARMERS + 1),
    "location": np.random.choice(LOCATIONS, N_FARMERS),
    "crop": np.random.choice(CROPS, N_FARMERS),
    "avg_yield_kg": np.random.randint(500, 2500, N_FARMERS),
    "reliability_score": np.round(np.random.uniform(0.6, 0.95, N_FARMERS), 2)
})

# -----------------------------
# MARKET PRICE SIMULATION
# -----------------------------
price_records = []

for crop in CROPS:
    base_price = {"maize": 250, "rice": 400, "tomato": 300}[crop]
    
    seasonal_effect = np.sin(np.linspace(0, 3 * np.pi, len(dates))) * 40
    trend = np.linspace(0, 60, len(dates))
    noise = np.random.normal(0, 15, len(dates))
    
    for market in MARKETS:
        market_multiplier = np.random.uniform(0.95, 1.1)
        prices = base_price + seasonal_effect + trend + noise
        prices = prices * market_multiplier
        
        for d, p in zip(dates, prices):
            price_records.append([d, market, crop, round(max(p, 50), 2)])

daily_market_prices = pd.DataFrame(
    price_records,
    columns=["date", "market", "crop", "price_per_kg"]
)

# -----------------------------
# SUPPLY RECORDS
# -----------------------------
supply_records = []

for _, farmer in farmers.iterrows():
    for d in dates:
        if random.random() < farmer["reliability_score"]:
            quantity = np.random.normal(
                farmer["avg_yield_kg"],
                farmer["avg_yield_kg"] * 0.25
            )
            supply_records.append([
                farmer["farmer_id"],
                d,
                farmer["crop"],
                max(int(quantity), 0)
            ])

supply_records = pd.DataFrame(
    supply_records,
    columns=["farmer_id", "date", "crop", "quantity_available"]
)

# -----------------------------
# SALES (DEMAND-DRIVEN)
# -----------------------------
sales_records = []

for crop in CROPS:
    for market in MARKETS:
        crop_prices = daily_market_prices[
            (daily_market_prices["crop"] == crop) &
            (daily_market_prices["market"] == market)
        ]
        
        base_demand = {"maize": 4000, "rice": 3000, "tomato": 2000}[crop]
        
        for _, row in crop_prices.iterrows():
            demand = np.random.normal(base_demand, base_demand * 0.2)
            quantity_sold = max(int(demand), 0)
            
            sales_records.append([
                row["date"],
                market,
                crop,
                quantity_sold,
                row["price_per_kg"] * np.random.uniform(1.05, 1.2)
            ])

sales = pd.DataFrame(
    sales_records,
    columns=["date", "market", "crop", "quantity_sold", "selling_price"]
)

# -----------------------------
# TRANSPORT COSTS
# -----------------------------
routes = []

route_id = 1
for loc in LOCATIONS:
    for market in MARKETS:
        distance = np.random.randint(80, 450)
        cost = distance * np.random.uniform(1.8, 2.5)
        capacity = np.random.randint(3000, 8000)
        
        routes.append([
            route_id,
            loc,
            market,
            distance,
            round(cost, 2),
            capacity
        ])
        route_id += 1

transport_costs = pd.DataFrame(
    routes,
    columns=[
        "route_id",
        "origin_location",
        "market",
        "distance_km",
        "cost_per_trip",
        "capacity_kg"
    ]
)

# -----------------------------
# SAVE DATA
# -----------------------------
farmers.to_csv("data/raw/farmers.csv", index=False)
daily_market_prices.to_csv("data/raw/daily_market_prices.csv", index=False)
supply_records.to_csv("data/raw/supply_records.csv", index=False)
sales.to_csv("data/raw/sales.csv", index=False)
transport_costs.to_csv("data/raw/transport_costs.csv", index=False)

print("✅ Data simulation complete.")