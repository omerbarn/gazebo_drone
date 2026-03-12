# ArduPilot Autonomous Drone Simulation (ROS2 + Gazebo Sim + MAVROS + Pymavlink)

This project provides a comprehensive simulation stack for autonomous drones using **ArduPilot SITL**, **Gazebo Sim (Harmonic)**, **ROS2 Humble**, **MAVROS**, and a **Python (Pymavlink)** controller.

## Architecture

The system consists of four main Docker containers:

1.  **ArduPilot SITL**: The flight controller running ArduCopter firmware.
2.  **Gazebo Sim**: The physics engine and environment (Iris quadcopter).
3.  **MAVROS**: The ROS2 bridge to MAVLink (for future ROS2 expansion).
4.  **Pymavlink Controller**: The primary autonomous controller using a solid OOP design.

### High-level Communication

Gazebo Sim (Physics) <-> ArduPilot SITL (FCU) <-> Pymavlink Controller (Logic)
                                         ^
                                         |
                                       MAVROS (ROS2 Bridge)

## Technology Stack

*   **ArduPilot**: Copter-4.5 SITL
*   **Gazebo Sim**: Harmonic (with GPU support)
*   **ROS2**: Humble
*   **MAVROS**: ROS2 Humble version
*   **Python**: Pymavlink, numpy

## Python Controller Design

The controller is designed with a two-tier architecture:

*   **DroneManager**: Handles low-level MAVLink communication, mode changes (GUIDED, MANUAL, etc.), and command sending (RPY, RC Overrides, Angular Acceleration).
*   **MissionController**: Manages high-level mission logic and flight patterns.

## Getting Started

### Prerequisites

*   Docker and Docker Compose
*   NVIDIA Container Toolkit (for GPU support in Gazebo)

### Running the Simulation

```bash
docker-compose up
```

## Control Modes Supported

*   **GUIDED**: Position and velocity control.
*   **MANUAL/STABILIZE**: Direct RC or attitude control.
*   **RC Override**: Simulating transmitter inputs.
*   **RPY/Angular Accel**: High-frequency attitude and acceleration targets.

## License

MIT License
