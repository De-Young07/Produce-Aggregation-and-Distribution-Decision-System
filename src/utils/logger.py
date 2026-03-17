import logging
import os

def setup_logger():

    os.makedirs("data/logs", exist_ok=True)

    logger = logging.getLogger("pipeline_logger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("data/logs/pipeline.log")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger