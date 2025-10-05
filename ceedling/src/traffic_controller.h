#ifndef TRAFFIC_CONTROLLER_H
#define TRAFFIC_CONTROLLER_H

#include <stdint.h>

void TrafficController_Init(void);
void TrafficController_Tick(uint32_t ms_elapsed); // The "engine" of the FSM
void TrafficController_PedestrianButtonPressed(void);

#endif // TRAFFIC_CONTROLLER_H