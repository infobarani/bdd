#include "hal_traffic_lights.h"

// Harness Function Signatures
void Harness_Init(void);
void Harness_Tick(uint32_t ms);
void Harness_PressButton(void);
LightState_t Harness_GetMainLight(void);
LightState_t Harness_GetSideLight(void);
PedestrianSignal_t Harness_GetPedestrianSignal(void);