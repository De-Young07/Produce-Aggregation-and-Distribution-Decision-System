install:
	pip install -r requirements.txt

phase1:
	python run_pipeline.py --phase phase1

phase2:
	python run_pipeline.py --phase phase2

run:
	python run_pipeline.py

clean:
	rm -rf data/features/*
	rm -rf data/processed/*