# Traffic Light Controller BDD Project

This project demonstrates Behavior-Driven Development (BDD) for an embedded C traffic light controller using Behave (Python) and Ceedling (C testing framework).

## Project Structure

```
bdd/
├── ceedling/                # Ceedling project for our C code
│   ├── project.yml          # Ceedling configuration
│   ├── src/                 # Our C source code
│   │   ├── traffic_controller.c
│   │   ├── traffic_controller.h
│   │   └── hal_traffic_lights.h # Hardware Abstraction Layer (to be mocked)
│   └── test/                # Our C tests (including the BDD harness)
│       └── test_harness.c
├── features/                # Behave project
│   ├── environment.py       # Behave setup/teardown hooks
│   ├── traffic_light.feature # Our Gherkin specification
│   └── steps/
│       └── traffic_steps.py   # Python step definitions
└── Makefile                 # A simple Makefile to tie it all together
```

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

## Build the shared library
    This command will first run Ceedling to compile the C code and generate the necessary object files, then it will link them into a shared library for Python.
    
    ```bash
    make shared_lib
    ```

## Running Tests

To run the BDD test suite, ensure your Python virtual environment is activated and then execute:

```bash
behave
```

You should see output indicating that all scenarios and steps are passing.
