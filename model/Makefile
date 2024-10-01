CC=gcc
CFLAGS=-MMD -Wall -Werror -g

BUILD_DIR=build
SRCS=test.c model.c
HEADERS=model.h list.h
OBJECTS=$(foreach src, $(SRCS), $(BUILD_DIR)/$(src:.c=.o))

test: $(BUILD_DIR) $(OBJECTS) $(HEADERS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o test

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	-rm -rf build
	-rm -f test

-include $(BUILD_DIR)/*.d