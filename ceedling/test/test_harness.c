#include "unity.h"
#include "traffic_controller.h"

// IMPORTANT: Include the MOCK version of the HAL
#include "mock_hal_traffic_lights.h"

// --- Globals to store the last known state of our "hardware" ---
// The mock functions will update these variables.
static LightState_t g_ns_light;
static LightState_t g_ew_light;
static PedestrianSignal_t g_ped_signal;

// --- Custom Mock implementations ---
// We tell CMock to call these functions whenever the real HAL functions would be called.
// This allows us to "capture" the output of the controller.
void mock_Hal_SetNorthSouthLight(LightState_t state, int num_calls) {
    g_ns_light = state;
}
void mock_Hal_SetEastWestLight(LightState_t state, int num_calls) {
    g_ew_light = state;
}
void mock_Hal_SetPedestrianSignal(PedestrianSignal_t signal, int num_calls) {
    g_ped_signal = signal;
}


// --- These are the functions Python/CFFI will call ---

void Harness_Init(void) {
    // Set up our mock callbacks BEFORE initializing the controller
    Hal_SetNorthSouthLight_StubWithCallback(mock_Hal_SetNorthSouthLight);
    Hal_SetEastWestLight_StubWithCallback(mock_Hal_SetEastWestLight);
    Hal_SetPedestrianSignal_StubWithCallback(mock_Hal_SetPedestrianSignal);
    
    TrafficController_Init();
}

void Harness_Tick(uint32_t ms) {
    TrafficController_Tick(ms);
}

void Harness_PressButton(void) {
    TrafficController_PedestrianButtonPressed();
}

// --- These are the "getter" functions for Python to check the state ---

LightState_t Harness_GetNorthSouthLight(void) {
    return g_ns_light;
}

LightState_t Harness_GetEastWestLight(void) {
    return g_ew_light;
}

PedestrianSignal_t Harness_GetPedestrianSignal(void) {
    return g_ped_signal;
}
