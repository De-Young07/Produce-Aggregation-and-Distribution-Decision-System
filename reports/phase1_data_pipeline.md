# Phase 1 — Data Simulation and Ingestion

## Objective

Establish the foundational data infrastructure for the agricultural
analytics pipeline.

The phase focuses on generating synthetic market data and loading
it into a structured database environment.

---

## Pipeline Components

1. Data Simulation
2. Data Validation
3. Data Storage
4. Logging
5. Documentation

---

## Datasets Generated

### Price Data

Contains daily crop prices across markets.

Columns

date  
crop  
market  
price_per_kg

---

### Demand Data

Estimated market demand for each crop.

Columns

date  
crop  
market  
demand

---

### Supply Data

Production supplied by farmers.

Columns

date  
farmer_id  
crop  
quantity_supplied

---

### Transport Costs

Logistics cost and transport capacity.

Columns

origin  
market  
cost_per_kg  
capacity

---

### Sales Data

Observed market transactions.

Columns

date  
crop  
market  
quantity  
revenue

---

## Validation Rules

- No missing values
- No empty datasets
- All tables conform to schema

---

## Output

CSV datasets in

data/raw/

Database tables in

agri_pipeline database

---

## Logs

Pipeline execution logs stored in

data/logs/pipeline.log

---

## Reproducibility

All parameters controlled via

config/config.yaml