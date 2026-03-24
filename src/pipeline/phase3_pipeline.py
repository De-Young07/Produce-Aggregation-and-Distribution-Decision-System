from src.forecasting.train_models import train_models
from src.forecasting.evaluate_models import evaluate_models
from src.forecasting.forecast import generate_forecasts
from src.forecasting.load_forecasts_to_mysql import load_forecasts_to_mysql
from src.utils.logger import setup_logger

logger = setup_logger()

def run_phase3():

    logger.info("Phase 3 started")

    train_models()

    evaluate_models()

    generate_forecasts()

    load_forecasts_to_mysql()

    logger.info("Phase 3 completed")