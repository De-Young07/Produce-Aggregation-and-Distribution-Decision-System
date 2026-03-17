from src.pipeline.phase1_pipeline import run_phase1
from src.pipeline.phase2_pipeline import run_phase2

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--phase", type=str)

args = parser.parse_args()

if args.phase == "phase1":
    run_phase1()

elif args.phase == "phase2":
    run_phase2()

else:
    run_phase1()
    run_phase2()