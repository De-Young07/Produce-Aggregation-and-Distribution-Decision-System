from pathlib import Path
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import os


def optimize_distribution():

    df = pd.read_csv("data/optimization/optimization_input.csv")

    model = LpProblem("Supply_Optimization", LpMaximize)

    decision_vars = {}

    for i, row in df.iterrows():

        key = f"{row['crop']}_{row['market']}"

        decision_vars[key] = LpVariable(key, lowBound=0)

    # Objective function
    model += lpSum(
        decision_vars[f"{row['crop']}_{row['market']}"] *
        (row["forecast_price"] - row["transport_cost"])
        for _, row in df.iterrows()
    )

    # Supply constraints
    for crop in df["crop"].unique():

        model += lpSum(
            decision_vars[f"{row['crop']}_{row['market']}"]
            for _, row in df[df["crop"] == crop].iterrows()
        ) <= df[df["crop"] == crop]["supply"].iloc[0]

    # Demand constraints (soft cap)
    for _, row in df.iterrows():

        key = f"{row['crop']}_{row['market']}"

        model += decision_vars[key] <= row["supply"]

    model.solve()

    results = []

    for key, var in decision_vars.items():

        crop, market = key.split("_")

        results.append([crop, market, var.value()])

    result_df = pd.DataFrame(
        results,
        columns=["crop", "market", "optimal_quantity"]
    )

    os.makedirs("data/optimization", exist_ok=True)

    result_df.to_csv("data/optimization/optimal_distribution.csv", index=False)

    print("Optimization complete")

    return result_df