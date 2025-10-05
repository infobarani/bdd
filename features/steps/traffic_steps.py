from behave import given, when, then
from cffi import FFI

# --- CFFI Bridge Setup ---
ffi = FFI()
ffi.cdef("""
    // C Enums
    typedef enum { LIGHT_STATE_RED, LIGHT_STATE_YELLOW, LIGHT_STATE_GREEN, LIGHT_STATE_OFF } LightState_t;
    typedef enum { PED_SIGNAL_DONT_WALK, PED_SIGNAL_WALK, PED_SIGNAL_FLASHING_DONT_WALK } PedestrianSignal_t;

    // Harness Function Signatures
    void Harness_Init(void);
    void Harness_Tick(uint32_t ms);
    void Harness_PressButton(void);
    LightState_t Harness_GetNorthSouthLight(void);
    LightState_t Harness_GetEastWestLight(void);
    PedestrianSignal_t Harness_GetPedestrianSignal(void);
""")

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
    actual = lib.Harness_GetNorthSouthLight()
    assert actual == expected, f"Main Light: Expected {color}, but got {actual}"

@then('the side light should be {color}')
def step_impl(context, color):
    expected = LIGHT_MAP[color]
    actual = lib.Harness_GetEastWestLight()
    assert actual == expected, f"Side Light: Expected {color}, but got {actual}"

@then('all vehicle lights should be Red')
def step_impl(context):
    assert lib.Harness_GetNorthSouthLight() == lib.LIGHT_STATE_RED
    assert lib.Harness_GetEastWestLight() == lib.LIGHT_STATE_RED

@then('the pedestrian signal should be {signal}')
def step_impl(context, signal):
    expected = PED_MAP[signal]
    actual = lib.Harness_GetPedestrianSignal()
    assert actual == expected, f"Ped Signal: Expected {signal}, but got {actual}"
