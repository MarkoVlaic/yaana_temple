.PHONY: build
build:
	python ./build_model.py

.PHONY: build
clean:
	rm *.o *.so *.c

.PHONY: run-benchmark
run-benchmark: export LD_LIBRARY_PATH = ../model
run-benchmark:
	python ./benchmark.py