from src.data_simulation.simulate_prices import simulate_prices
from src.data_simulation.simulate_demand import simulate_demand
from src.data_simulation.simulate_supply import simulate_supply
from src.data_simulation.simulate_transport import simulate_transport
from src.data_simulation.simulate_sales import simulate_sales

from src.validation.validate_data import validate_dataset
from src.ingestion.load_to_sql import load_csv_to_mysql
from src.utils.logger import setup_logger

logger = setup_logger()

def run_phase1():

    logger.info("Phase 1 started")

    simulate_prices()
    simulate_demand()
    simulate_supply()
    simulate_transport()
    simulate_sales()

    datasets = {
        "data/raw/prices.csv":"prices",
        "data/raw/demand.csv":"demand",
        "data/raw/supply.csv":"supply",
        "data/raw/transport_costs.csv":"transport_costs",
        "data/raw/sales.csv":"sales"
    }

    for path, table in datasets.items():

        validate_dataset(path)

        load_csv_to_mysql(path, table)

        logger.info(f"{table} loaded successfully")

    logger.info("Phase 1 completed")