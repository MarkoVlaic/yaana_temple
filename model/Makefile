CC=gcc
CFLAGS=-MMD -Wall -g
LDFLAGS = -lm -lmodel -lstdc++

BUILD_DIR=build
LIB_MODEL_SRCS=model.c geom.c
LIB_CLIPPING_SRCS=clipping.cpp
EXE_SRCS=test.c benchmark.c fuzzer.c
HEADERS=model.h list.h geom.h
LIB_MODEL_OBJECTS=$(foreach src, $(LIB_MODEL_SRCS), $(BUILD_DIR)/lib_model/$(src:.c=.o))
LIB_CLIPPING_OBJECTS=$(foreach src, $(LIB_CLIPPING_SRCS), $(BUILD_DIR)/lib_clipping/$(src:.cpp=.o))
EXE_OBJECTS=$(foreach src, $(EXE_SRCS), $(BUILD_DIR)/exe/$(src:.c=.o))

all: benchmark test fuzzer libmodel.so

.PHONY: run-test
run-test: export LD_LIBRARY_PATH = $(shell pwd)
run-test:
	./test

.PHONY: debug-test
debug-test: export LD_LIBRARY_PATH = $(shell pwd)
debug-test:
	gdb ./test

.PHONY: mem-test
mem-test: export LD_LIBRARY_PATH = $(shell pwd)
mem-test:
	valgrind --leak-check=full ./test

.PHONY: run-benchmark
run-benchmark: export LD_LIBRARY_PATH = $(shell pwd)
run-benchmark:
	./benchmark

.PHONY: run-fuzzer
run-fuzzer: export LD_LIBRARY_PATH = $(shell pwd)
run-fuzzer:
	./fuzzer

test: $(BUILD_DIR) $(LIB_MODEL_OBJECTS) libmodel.so $(BUILD_DIR)/exe/test.o $(HEADERS)
	$(CC) $(BUILD_DIR)/exe/test.o -L$(shell pwd) $(LDFLAGS) -o test

benchmark: $(BUILD_DIR) $(LIB_MODEL_OBJECTS) libmodel.so $(BUILD_DIR)/exe/benchmark.o $(HEADERS)
	$(CC) $(BUILD_DIR)/exe/benchmark.o -L$(shell pwd) $(LDFLAGS) -o benchmark

fuzzer: $(BUILD_DIR) $(LIB_MODEL_OBJECTS) libmodel.so $(BUILD_DIR)/exe/fuzzer.o $(HEADERS)
	$(CC) $(BUILD_DIR)/exe/fuzzer.o -L$(shell pwd) $(LDFLAGS) -o fuzzer

libmodel.so: $(LIB_MODEL_OBJECTS) $(BUILD_DIR)/lib_clipping/libclipping.o $(HEADERS)
	g++ -lstdc++ -shared $^ -o $@
	$(CC) -E model.h > $(BUILD_DIR)/lib_model/model.h.preprocessed

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/lib_model
	mkdir -p $(BUILD_DIR)/lib_clipping
	mkdir -p $(BUILD_DIR)/exe

$(BUILD_DIR)/lib_clipping/libclipping.o: $(LIB_CLIPPING_SRCS) contourklip.hpp clipping.h
	g++ $(CFLAGS) -c -fPIC $< -o $@

$(BUILD_DIR)/lib_model/%.o: %.c
	$(CC) $(CFLAGS) -fpic -c $< -o $@

$(BUILD_DIR)/exe/%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	-rm -rf build
	-rm -f test
	-rm -f benchmark
	-rm -f fuzzer
	-rm -f libmodel.so

-include $(BUILD_DIR)/*.d