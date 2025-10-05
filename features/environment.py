from cffi import FFI
import os

def before_all(context):
    # --- CFFI Bridge Setup ---
    ffi = FFI()

    # Read the C definitions from the CFFI-specific header file
    with open(os.path.join(os.path.dirname(__file__), 'steps', 'harness_for_cffi.h')) as f:
        ffi.cdef(f.read())

    # Load the shared library we built with our Makefile
    # Make sure the path is correct from where you run 'behave'
    context.lib = ffi.dlopen("ceedling/build/libharness.so") # Use .dll on Windows

    # --- Mappings from strings to our C enums for readability ---
    context.LIGHT_MAP = {
        "Red": context.lib.LIGHT_STATE_RED,
        "Yellow": context.lib.LIGHT_STATE_YELLOW,
        "Green": context.lib.LIGHT_STATE_GREEN,
    }
    context.PED_MAP = {
        "Walk": context.lib.PED_SIGNAL_WALK,
        "Don't Walk": context.lib.PED_SIGNAL_DONT_WALK,
        "Flashing Don't Walk": context.lib.PED_SIGNAL_FLASHING_DONT_WALK,
    }

    # Create reverse mappings for user-friendly error messages
    context.REVERSE_LIGHT_MAP = {v: k for k, v in context.LIGHT_MAP.items()}
    context.REVERSE_PED_MAP = {v: k for k, v in context.PED_MAP.items()}