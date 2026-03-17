# Phase 2 — SQL Feature Engineering and Time Series Dataset Builder

## Objective

Transform raw agricultural datasets into model-ready
time series datasets.

---

## Feature Engineering

The following features were generated:

price_per_kg  
demand  
total_supply  

Rolling averages:

price_ma7  
price_ma30

---

## Time-Series Construction

Each crop–market pair was converted into a separate
forecasting dataset.

Example:

maize_lagos_timeseries.csv  
rice_abuja_timeseries.csv  

---

## Feature Store

A centralized feature store was created to allow
consistent feature reuse across models.

Stored in:

data/features/store

---

## Outputs

Feature dataset:

data/features/market_features.csv

Time-series datasets:

data/processed/*.csv