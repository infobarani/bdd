## Project Purpose and Vision

This project was created to serve as a comprehensive, open-source blueprint for applying modern testing methodologies—specifically **Behavior-Driven Development (BDD)**—to embedded C projects. It aims to demystify functional testing for firmware developers, students, and engineers new to the field by providing a practical, end-to-end example.

### Core Objectives

The primary goal is to demonstrate a workflow that produces reliable, maintainable, and verifiable firmware. This is achieved through several key principles:

*   **Living Documentation:** Using Gherkin (`.feature` files), the system's requirements are written in plain English. These files are not just documentation; they are the executable test specifications, ensuring that the specification and the tests never go out of sync.
*   **Hardware-Independent Development:** By abstracting the hardware layer (HAL) and using mocks, the core controller logic can be developed and tested entirely on a host machine. This allows for **early firmware maturity** by simulating and validating new features long before physical hardware is available.
*   **A Single Source of Truth:** System parameters, like traffic light timings, are managed in a single `spec.csv` file. This data is automatically propagated to both the C source code (`spec.h`) and the BDD test files, eliminating the risk of inconsistencies.
*   **CI/CD Readiness:** The entire build and test process is scriptable via the `Makefile`, making it trivial to integrate into modern Continuous Integration/Continuous Deployment (CI/CD) pipelines.

### A Foundation for AI-Assisted Development & Agentic Testing

In the era of AI-assisted coding, robust and automated testing is more critical than ever. While AI coding agents (LLMs) accelerate development, they are also prone to introducing subtle bugs. This project's architecture provides the perfect **"stable test infrastructure"** to safely leverage AI, enabling a workflow known as **Agentic Testing**.

*   **A Feedback Mechanism for Autonomous Agents:** The `behave` test suite becomes another tool in the AI agent's toolkit. An autonomous agent can write code, run the tests, parse the human-readable output, and self-correct its code based on the feedback, iterating until all tests pass without direct human intervention.
*   **Leveraging LLM Strengths:** The Gherkin syntax used in `.feature` files is a form of structured, natural language. This is a format that Large Language Models (LLMs) excel at generating, making it easy for them to create new, valid test cases from high-level prompts.
*   **AI-Assisted Test Case Generation:** An AI agent can be prompted to formulate new test scenarios in Gherkin. This is a powerful technique for discovering edge cases that human developers might overlook. For example, one could prompt the agent: "Write a BDD scenario to test rapid, repeated presses of the pedestrian button."

This framework allows developers to harness the power of AI to both write code and enhance test coverage, all while using a deterministic, verifiable test suite to guarantee the system's correctness. It transforms development into a collaborative effort between human engineers and AI agents, building a foundation of trust for the final product.

## Project Workflow: From Requirement to Automated Test

This project is more than just a collection of files; it's a demonstration of a complete, modern workflow for embedded development. This section breaks down how each part of the project contributes to the final goal: creating reliable firmware that is automatically verified.

### Project Structure and Walkthrough

Here is a look at the key directories and how they interact with each other in the development and testing process.

```
.
├── utils/                # 1. The Single Source of Truth (spec.csv)
├── lib/                  # 2. The Firmware (Unit Under Test)
├── hal/                  # 3. The Hardware Abstraction Layer
├── ceedling/             # 4. The C-Level Test Harness & Mocks
├── features/             # 5. The BDD Test Specifications
└── Makefile              # 6. The Orchestrator
```

#### **1. `/utils` - The Single Source of Truth**

*   **Purpose:** This directory holds the master specification for all system timings (`spec.csv`). This is the starting point of our workflow.

    > **Note on Industry Practice:** For simplicity, this project uses a `spec.csv` file as the single source of truth. In a professional setting, this role would be filled by a more robust system, such as a formal **requirements management database** (e.g., JAMA Connect, IBM DOORS), a **specification control system**, or documents detailing **compliance specifications** (e.g., AUTOSAR timings, medical device standards). The key principle remains the same: parameters are managed in one central place and programmatically propagated to both the code and the tests to ensure consistency.

*   **Workflow:** When you run `make`, Python scripts in this directory read `spec.csv` and generate:
    *   `lib/spec.h`, injecting the timings directly into the C code.
    *   The final `.feature` files, injecting the same timings into the BDD tests.
*   **Key Takeaway:** This guarantees that our firmware and our tests are **always** using the exact same timing specifications.

#### **2. `/lib` - The Firmware (Unit Under Test)**

*   **Purpose:** This contains the core logic of our application, `traffic_controller.c`, which is a state machine written in pure C.
*   **Workflow:** The code is hardware-agnostic and only knows about high-level concepts like "set the main light to Green." It includes the generated `spec.h` to control its state transition timings.
*   **Key Takeaway:** This is the "Unit Under Test" (UUT). Our goal is to verify its behavior without needing to flash it to a physical microcontroller.

#### **3. `/hal` - The Hardware Abstraction Layer**

*   **Purpose:** The HAL (`hal_traffic_lights.h`) defines the *interface* (the "contract") between our application logic and the hardware.
*   **Workflow:** For testing purposes, we deliberately do **not** provide a hardware-specific implementation. Instead, we mock this interface.
*   **Key Takeaway:** The HAL is the critical boundary that decouples logic from hardware, enabling PC-based testing.

#### **4. `/ceedling` - The C-Level Test Harness & Mocks**

*   **Purpose:** This is the "bridge" that connects our high-level Python tests to our low-level C code.
*   **Workflow:**
    1.  **Mocking:** Ceedling automatically creates "mocks" (fake versions) of our HAL that record function calls instead of controlling hardware.
    2.  **Harness:** `test/test_harness.c` uses these mocks. When the firmware calls `Hal_SetMainLight()`, our harness intercepts this and stores the light's state in a variable.
    3.  **Exposure:** The harness exposes simple functions (`Harness_GetMainLight()`) that Python can call to read the state.
*   **Key Takeaway:** The harness acts as a translator, allowing Python to "press buttons" and "see" the state of the virtual lights.

#### **5. `/features` - The BDD Test Specifications**

*   **Purpose:** This is where we define the desired system behavior in plain English using the Gherkin syntax.
*   **Workflow:**
    1.  **Templates (`.feature.in`):** We write test scenarios here using placeholders like `{MAIN_GREEN_DURATION_SECONDS}`.
    2.  **Generation (`.feature`):** The `make` command populates these templates to create the final, executable test files.
    3.  **Step Definitions (`/steps/*.py`):** These Python files contain the code that runs for each Gherkin step, using the CFFI bridge to call our C harness and assert the results.
*   **Key Takeaway:** This directory connects human-readable requirements directly to the executable code that verifies the firmware.

#### **6. `Makefile` - The Orchestrator**

*   **Purpose:** The `Makefile` ties everything together into simple commands.
*   **Workflow:** `make` runs all necessary steps in the correct order: generate source files from the spec, then compile the C code and harness into a shared library for Python to use. `behave` (or `make test`) then runs the BDD test suite against this library.

### Automating with CI/CD: The Quality Gateway

#### What is CI/CD?

CI/CD stands for **Continuous Integration** and **Continuous Deployment/Delivery**. In simple terms, it's the practice of automating your build and testing process.

*   **Continuous Integration (CI):** Think of it as an automated quality inspector. Every time a developer pushes a code change, a server automatically builds the project and runs all the tests. If any test fails, the team is immediately notified. The goal is to catch bugs early and prevent them from being merged into the main codebase.

#### How This Project Enables CI/CD

This project is perfectly structured for CI because our entire test suite can be run from the command line with two commands: `make` and `behave`. Because the tests are self-contained and require no physical hardware, they can run on any standard CI server (like GitHub Actions, GitLab CI, or Jenkins).

This setup ensures that any proposed code change automatically receives a clear "pass" or "fail" status, maintaining the stability and quality of your firmware at all times.

## Getting Started

### Development Environment

> **A Note for Windows Users**
>
> This project and its tooling (`make`, `gcc`, etc.) are designed to run in a Linux-based environment. For users on Windows, the highly recommended approach is to use the **Windows Subsystem for Linux (WSL)**. WSL provides a complete Linux environment that runs directly on Windows, allowing you to use native Linux command-line tools and applications without the need for a separate virtual machine.
>
> This approach mirrors common industry practices where development and build systems are standardized on Linux, typically running inside **containers** (like Docker). By using WSL locally, you are adopting a workflow that is consistent with modern CI/CD pipelines, ensuring that your code behaves predictably and eliminating "it works on my machine" problems.

### Prerequisites

*   **Ruby and RubyGems:** Required for Ceedling.
    ```bash
    sudo apt-get update && sudo apt-get install ruby-full
    ```
*   **Ceedling:** Install via RubyGems.
    ```bash
    sudo gem install ceedling
    ```
*   **Python 3 and pip:** Required for Behave and CFFI. It is highly recommended to use a Python virtual environment.
    ```bash
    sudo apt-get install python3-pip python3.12-venv
    ```
*   **Install Python dependencies:**
    ```bash
    # python3 -m venv venv
    # source venv/bin/activate
    pip install behave cffi
    ```

### Building the Project

To build the project and generate all necessary files, simply run `make`:

```bash
make
```

This command will:

1.  Run the Python scripts in `utils/` to generate `lib/spec.h` and the `.feature` files.
2.  Run Ceedling to compile the C code and generate the test harness objects.
3.  Link all object files into a shared library (`ceedling/build/libharness.so`) for Python to use.

### Running Tests

To run the BDD test suite, execute:

```bash
behave
```

You should see output indicating that all scenarios and steps are passing.
