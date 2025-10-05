#include "traffic_controller.h"
#include "hal_traffic_lights.h" // We depend on the HAL interface

typedef enum {
    STATE_MAIN_GREEN,
    STATE_MAIN_YELLOW,
    STATE_SIDE_GREEN,
    STATE_SIDE_YELLOW,
    STATE_ALL_RED_CLEARANCE,
    STATE_PEDESTRIAN_WALK,
    STATE_PEDESTRIAN_FLASH,
} ControllerState_t;

// Module-level static variables
static ControllerState_t currentState;
static uint32_t timer_ms;
static bool pedestrian_request_pending;
static ControllerState_t next_state_after_clearance;

// State Durations
#include "spec.h"


void TrafficController_Init(void) {
    currentState = STATE_MAIN_GREEN;
    timer_ms = 0;
    pedestrian_request_pending = false;
    Hal_SetMainLight(LIGHT_STATE_GREEN);
    Hal_SetSideLight(LIGHT_STATE_RED);
    Hal_SetPedestrianSignal(PED_SIGNAL_DONT_WALK);
}

void TrafficController_PedestrianButtonPressed(void) {
    // Only accept a request if one isn't already pending
    if (!pedestrian_request_pending) {
        pedestrian_request_pending = true;
    }
}

void TrafficController_Tick(uint32_t ms_elapsed) {
    timer_ms += ms_elapsed;

    switch (currentState) {
        case STATE_MAIN_GREEN:
            if (timer_ms >= MAIN_GREEN_DURATION_MS) {
                currentState = STATE_MAIN_YELLOW;
                timer_ms = 0;
                Hal_SetMainLight(LIGHT_STATE_YELLOW);
            }
            break;

        case STATE_MAIN_YELLOW:
            if (timer_ms >= MAIN_YELLOW_DURATION_MS) {
                currentState = STATE_ALL_RED_CLEARANCE;
                timer_ms = 0;
                Hal_SetMainLight(LIGHT_STATE_RED);
                
                // Decide what to do after the red clearance
                if (pedestrian_request_pending) {
                    next_state_after_clearance = STATE_PEDESTRIAN_WALK;
                } else {
                    next_state_after_clearance = STATE_SIDE_GREEN;
                }
            }
            break;

        case STATE_ALL_RED_CLEARANCE:
            if (timer_ms >= ALL_RED_DURATION_MS) {
                currentState = next_state_after_clearance;
                timer_ms = 0;
                // Activate the next state's lights
                if (currentState == STATE_SIDE_GREEN) {
                    Hal_SetSideLight(LIGHT_STATE_GREEN);
                } else if (currentState == STATE_PEDESTRIAN_WALK) {
                    Hal_SetPedestrianSignal(PED_SIGNAL_WALK);
                    pedestrian_request_pending = false; // Consume the request
                } else if (currentState == STATE_MAIN_GREEN) {
                    Hal_SetMainLight(LIGHT_STATE_GREEN);
                }
            }
            break;
            
        case STATE_SIDE_GREEN:
            if (timer_ms >= SIDE_GREEN_DURATION_MS) {
                currentState = STATE_SIDE_YELLOW;
                timer_ms = 0;
                Hal_SetSideLight(LIGHT_STATE_YELLOW);
            }
            break;
        
        case STATE_SIDE_YELLOW:
            if (timer_ms >= SIDE_YELLOW_DURATION_MS) {
                currentState = STATE_ALL_RED_CLEARANCE;
                timer_ms = 0;
                Hal_SetSideLight(LIGHT_STATE_RED);
                next_state_after_clearance = STATE_MAIN_GREEN; // Next is always main green
            }
            break;
            
        case STATE_PEDESTRIAN_WALK:
            if (timer_ms >= PED_WALK_DURATION_MS) {
                currentState = STATE_PEDESTRIAN_FLASH;
                timer_ms = 0;
                Hal_SetPedestrianSignal(PED_SIGNAL_FLASHING_DONT_WALK);
            }
            break;

        case STATE_PEDESTRIAN_FLASH:
            if (timer_ms >= PED_FLASH_DURATION_MS) {
                currentState = STATE_ALL_RED_CLEARANCE; // Go to clearance before side green
                timer_ms = 0;
                Hal_SetPedestrianSignal(PED_SIGNAL_DONT_WALK);
                next_state_after_clearance = STATE_SIDE_GREEN;
            }
            break;
    }
}