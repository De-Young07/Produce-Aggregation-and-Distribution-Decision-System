from src.feature_engineering.run_sql_script import run_sql_script
from src.feature_engineering.sql_features import extract_feature_table
from src.feature_engineering.build_time_series import build_time_series
from src.feature_engineering.feature_store import register_features
from src.utils.logger import setup_logger

logger = setup_logger()

def run_phase2():

    logger.info("Phase 2 started")

    run_sql_script()

    extract_feature_table()

    build_time_series()

    register_features()

    logger.info("Phase 2 completed")