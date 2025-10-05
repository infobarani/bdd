from behave import given, when, then
from cffi import FFI
import os
import re

# --- CFFI Bridge Setup ---
ffi = FFI()

# Read the C definitions from the header files
harness_header_path = os.path.join(os.path.dirname(__file__), '..', '..', 'ceedling', 'test', 'test_harness.h')
hal_header_path = os.path.join(os.path.dirname(__file__), '..', '..', 'hal', 'hal_traffic_lights.h')

with open(hal_header_path) as f:
    hal_content = f.read()

with open(harness_header_path) as f:
    harness_content = f.read()

# Extract enum definitions from hal_content
enums = "".join(re.findall(r"typedef enum \{.*?\} \w+_t;", hal_content, re.DOTALL))

# Remove the include from harness_content
harness_content = re.sub(r'#include ".*"', '', harness_content)

ffi.cdef(enums)
ffi.cdef(harness_content)

# Load the shared library we built with our Makefile
# Make sure the path is correct from where you run 'behave'
lib = ffi.dlopen("ceedling/build/libharness.so") # Use .dll on Windows

# --- Mappings from strings to our C enums for readability ---
LIGHT_MAP = {
    "Red": lib.LIGHT_STATE_RED,
    "Yellow": lib.LIGHT_STATE_YELLOW,
    "Green": lib.LIGHT_STATE_GREEN,
}
PED_MAP = {
    "Walk": lib.PED_SIGNAL_WALK,
    "Don't Walk": lib.PED_SIGNAL_DONT_WALK,
    "Flashing Don't Walk": lib.PED_SIGNAL_FLASHING_DONT_WALK,
}

# --- Step Definitions ---

@given('the traffic controller is initialized')
def step_impl(context):
    lib.Harness_Init()

@when('{seconds:d} second passes')
@when('{seconds:d} seconds pass')
def step_impl(context, seconds):
    # Call Tick() in small increments to simulate time
    ms_to_pass = seconds * 1000
    tick_increment_ms = 10
    for _ in range(ms_to_pass // tick_increment_ms):
        lib.Harness_Tick(tick_increment_ms)

@when('the pedestrian button is pressed')
def step_impl(context):
    lib.Harness_PressButton()

@then('the main light should be {color}')
def step_impl(context, color):
    expected = LIGHT_MAP[color]
    actual = lib.Harness_GetMainLight()
    assert actual == expected, f"Main Light: Expected {color}, but got {actual}"

@then('the side light should be {color}')
def step_impl(context, color):
    expected = LIGHT_MAP[color]
    actual = lib.Harness_GetSideLight()
    assert actual == expected, f"Side Light: Expected {color}, but got {actual}"

@then('all vehicle lights should be Red')
def step_impl(context):
    assert lib.Harness_GetMainLight() == lib.LIGHT_STATE_RED
    assert lib.Harness_GetSideLight() == lib.LIGHT_STATE_RED

@then('the pedestrian signal should be {signal}')
def step_impl(context, signal):
    expected = PED_MAP[signal]
    actual = lib.Harness_GetPedestrianSignal()
    assert actual == expected, f"Ped Signal: Expected {signal}, but got {actual}"