from src.optimization.build_dataset import build_optimization_dataset
from src.optimization.optimize_distribution import optimize_distribution
from src.optimization.load_optimization_to_mysql import load_optimization_results
from src.utils.logger import setup_logger

logger = setup_logger()

def run_phase4():

    logger.info("Phase 4 started")

    build_optimization_dataset()

    optimize_distribution()

    load_optimization_results()

    logger.info("Phase 4 completed")