# Traffic Controller Requirements

## 1. Project Background

This project specifies the requirements for a traffic controller system at a standard two-way intersection. The intersection has a main road and a side road. It also includes a pedestrian crossing with a signal and a request button.

## 2. High-Level Requirements

*   The system shall manage the flow of traffic by alternating between the main and side roads.
*   The system shall ensure that conflicting traffic is never allowed to proceed at the same time.
*   The system shall provide a safe crossing for pedestrians, separate from the flow of vehicular traffic.
*   The system shall default to allowing traffic on the main road to proceed.

## 3. Traffic Light and Pedestrian Signal Behavior

The system shall cycle through the following states, with timings in seconds:

| State                      | Main Road         | Side Road         | Pedestrian Signal | Duration (seconds) |
| -------------------------- | ----------------- | ----------------- | ------------------- | ------------------ |
| 1. Main Road Green         | Green             | Red               | Don't Walk          | 20                 |
| 2. Main Road Yellow        | Yellow            | Red               | Don't Walk          | 4                  |
| 3. All Red Clearance       | Red               | Red               | Don't Walk          | 2                  |
| 4. Side Road Green         | Red               | Green             | Don't Walk          | 10                 |
| 5. Side Road Yellow        | Red               | Yellow            | Don't Walk          | 4                  |
| 6. All Red Clearance       | Red               | Red               | Don't Walk          | 2                  |

## 4. Pedestrian Crossing

*   When a pedestrian presses the crossing button, the system shall initiate a pedestrian crossing cycle after the main road traffic has been stopped.
*   The pedestrian crossing cycle shall have the following states:

| State                      | Main Road         | Side Road         | Pedestrian Signal       | Duration (seconds) |
| -------------------------- | ----------------- | ----------------- | ----------------------- | ------------------ |
| 1. Pedestrian Walk         | Red               | Red               | Walk                    | 10                 |
| 2. Pedestrian Flash        | Red               | Red               | Flashing Don't Walk | 6                  |
| 3. All Red Clearance       | Red               | Red               | Don't Walk              | 2                  |

*   After the pedestrian crossing cycle is complete, the system shall proceed to the "Side Road Green" state.
