# Makefile to build the shared library for Behave/CFFI

# Adjust for your OS
ifeq ($(OS),Windows_NT)
    TARGET_LIB = ceedling/build/libharness.dll
    CC = gcc
else
    TARGET_LIB = ceedling/build/libharness.so
    CC = gcc
endif

# These are the object files Ceedling creates that we need.
# It includes our code, the harness, and the mock HAL.
OBJECTS = \
    ceedling/build/test/out/test_harness/test_harness.o \
    ceedling/build/test/out/test_harness/traffic_controller.o \
    ceedling/build/test/out/test_harness/mock_hal_traffic_lights.o \
    ceedling/build/test/out/test_harness/unity.o \
    ceedling/build/test/out/test_harness/cmock.o \
    ceedling/build/test/out/test_harness/test_harness_runner.o

# Phony targets
.PHONY: all clean shared_lib generate

all: shared_lib

# Rule to build the shared library
$(TARGET_LIB): $(OBJECTS)
	$(CC) -shared -o $@ $(OBJECTS)

# This target first runs ceedling to generate the .o files, then calls the build rule.
shared_lib: generate
	@echo "--- 1. Running Ceedling to generate object files... ---"
	cd ceedling && ceedling test:all > /dev/null 2>&1 || ceedling test:all
	@echo "--- 2. Linking object files into a shared library... ---"
	$(MAKE) $(TARGET_LIB)
	@echo "--- Done. Shared library created at $(TARGET_LIB) ---"

generate:
	@echo "--- 0. Generating spec.h and traffic_light.feature from spec.csv... ---"
	cd utils && python3 generate_spec_h.py
	cd utils && python3 generate_feature.py

clean:
	cd ceedling && ceedling clobber
	rm -f $(TARGET_LIB)
