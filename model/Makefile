CC=gcc
CFLAGS=-MMD -Wall -Werror -g
LDFLAGS = -lm -lmodel

BUILD_DIR=build
LIB_SRCS=model.c geom.c
EXE_SRCS=test.c
HEADERS=model.h list.h geom.h
LIB_OBJECTS=$(foreach src, $(LIB_SRCS), $(BUILD_DIR)/lib/$(src:.c=.o))
EXE_OBJECTS=$(foreach src, $(EXE_SRCS), $(BUILD_DIR)/exe/$(src:.c=.o))

all: test libmodel.so

.PHONY: run-test
run-test: export LD_LIBRARY_PATH = $(shell pwd)
run-test:
	./test

.PHONY: debug-test
debug-test: export LD_LIBRARY_PATH = $(shell pwd)
debug-test:
	gdb ./test


test: $(BUILD_DIR) $(LIB_OBJECTS) libmodel.so $(EXE_OBJECTS) $(HEADERS)
	$(CC) $(EXE_OBJECTS) -L$(shell pwd) $(LDFLAGS) -o test

libmodel.so: $(LIB_OBJECTS) $(HEADERS)
	gcc -shared $^ -o $@
	gcc -E model.h > $(BUILD_DIR)/lib/model.h.preprocessed

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/lib
	mkdir -p $(BUILD_DIR)/exe

$(BUILD_DIR)/lib/%.o: %.c
	$(CC) $(CFLAGS) -fpic -c $< -o $@

$(BUILD_DIR)/exe/%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	-rm -rf build
	-rm -f test
	-rm -f libmodel.so

-include $(BUILD_DIR)/*.d