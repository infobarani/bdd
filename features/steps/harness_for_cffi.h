// C Enums
typedef enum { LIGHT_STATE_RED, LIGHT_STATE_YELLOW, LIGHT_STATE_GREEN, LIGHT_STATE_OFF } LightState_t;
typedef enum { PED_SIGNAL_DONT_WALK, PED_SIGNAL_WALK, PED_SIGNAL_FLASHING_DONT_WALK } PedestrianSignal_t;

// Harness Function Signatures
void Harness_Init(void);
void Harness_Tick(uint32_t ms);
void Harness_PressButton(void);
LightState_t Harness_GetMainLight(void);
LightState_t Harness_GetSideLight(void);
PedestrianSignal_t Harness_GetPedestrianSignal(void);
