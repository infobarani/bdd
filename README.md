# Traffic Light Controller BDD Project

This project demonstrates Behavior-Driven Development (BDD) for an embedded C traffic light controller using Behave (Python) and Ceedling (C testing framework).

## Project Structure

```
bdd/
├── ceedling/                # Ceedling project for our C code
│   ├── project.yml          # Ceedling configuration
│   └── test/                # Our C tests (including the BDD harness)
│       ├── test_harness.c
│       └── test_harness.h
├── features/                # Behave project
│   ├── environment.py       # Behave setup/teardown hooks
│   ├── traffic_light.feature.in # Gherkin specification template
│   └── steps/
│       └── traffic_steps.py   # Python step definitions
├── lib/
│   ├── traffic_controller.c
│   ├── traffic_controller.h
│   └── spec.h               # Generated header with traffic light timings
├── hal/
│   └── hal_traffic_lights.h
├── utils/
│   ├── generate_feature.py    # Script to generate .feature from .feature.in
│   ├── generate_spec_h.py     # Script to generate spec.h from spec.csv
│   └── spec.csv               # CSV file with traffic light timings
└── Makefile                 # A simple Makefile to tie it all together
```

## How it Works

The core idea is to have a single source of truth for the traffic light timings, which is the `utils/spec.csv` file. This file is used to:

1.  Generate the `lib/spec.h` header file, which is used by the C code.
2.  Generate the `features/traffic_light.feature` file, which is used by Behave to run the BDD tests.

This ensures that the C code and the BDD tests are always in sync.

## Setup Instructions

### Prerequisites

*   **Ruby and RubyGems:** Required for Ceedling.
    ```bash
    sudo apt-get update
    sudo apt-get install ruby-full
    ```
*   **Ceedling:** Install via RubyGems.
    ```bash
    sudo gem install ceedling
    ```
*   **Python 3 and pip:** Required for Behave and CFFI.
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip python3.12-venv
    ```
*  **Install Python dependencies:**
    ```bash
    pip install behave cffi
    ```

## Build the project

To build the project, simply run `make`:

```bash
make
```

This command will:

1.  Run the python scripts in the `utils` directory to generate `lib/spec.h` and `features/traffic_light.feature`.
2.  Run Ceedling to compile the C code and generate the necessary object files.
3.  Link the object files into a shared library (`ceedling/build/libharness.so`) for Python to use.

## Running Tests

To run the BDD test suite, ensure your Python virtual environment is activated and then execute:

```bash
behave
```

You should see output indicating that all scenarios and steps are passing.

## Modifying Traffic Light Timings

To modify the traffic light timings, simply edit the `utils/spec.csv` file. The next time you run `make`, the changes will be automatically propagated to the C code and the BDD tests.