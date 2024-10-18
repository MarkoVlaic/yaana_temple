.PHONY: build
build:
	make -C model
	make -C model_module

.PHONY:dependencies
dependencies:
	python -m pip install -r requirements.txt

.PHONY: run-explorer
run-explorer: export LD_LIBRARY_PATH=./model/
run-explorer: export PYTHONPATH=.:model_module
run-explorer:
	python ./explorer/main.py

.PHONY: run-gpso
run-gpso: export LD_LIBRARY_PATH=./model/
run-gpso: export PYTHONPATH=.:model_module
run-gpso:
	python ./optimization/gpso.py

run-test:
	make -C model run-test

.PHONY: clean
clean:
	make -C model clean
	make -C model_module clean

	-rm -f scripts/cmc24_solution_*