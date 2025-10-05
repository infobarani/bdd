#ifndef HAL_TRAFFIC_LIGHTS_H
#define HAL_TRAFFIC_LIGHTS_H

#include <stdint.h>
#include <stdbool.h>

typedef enum {
    LIGHT_STATE_RED,
    LIGHT_STATE_YELLOW,
    LIGHT_STATE_GREEN,
    LIGHT_STATE_OFF
} LightState_t;

typedef enum {
    PED_SIGNAL_DONT_WALK,
    PED_SIGNAL_WALK,
    PED_SIGNAL_FLASHING_DONT_WALK,
} PedestrianSignal_t;

// --- Function Prototypes for Hardware Control ---

void Hal_SetMainLight(LightState_t state);
void Hal_SetSideLight(LightState_t state);
void Hal_SetPedestrianSignal(PedestrianSignal_t signal);

#endif // HAL_TRAFFIC_LIGHTS_H