from src.pipeline.phase1_pipeline import run_phase1
from src.pipeline.phase2_pipeline import run_phase2
from src.pipeline.phase3_pipeline import run_phase3
from src.pipeline.phase4_pipeline import run_phase4


def run_full_pipeline():

    run_phase1()
    run_phase2()
    run_phase3()
    run_phase4()

if __name__ == "__main__":

    run_full_pipeline()