# gazebo_drone
Gazebo drone with betaflight sitl

# Autonomous Drone Simulation (ROS2 + Gazebo + Betaflight SITL)

This project connects **ROS2**, **Gazebo**, **Betaflight SITL**, and **Python** to simulate and control a quadcopter autonomously using **MAVLink commands**.

The goal of the project is to demonstrate a full simulation pipeline where a drone can fly autonomously in **Gazebo** while running the **Betaflight flight controller in SITL**, and receive commands from a **Python controller through ROS2**.

Currently the drone performs a **circular flight trajectory** in the air using configurable control modes.

---

# Architecture



The system is composed of four main components:

| Component         | Role                                                         |
| ----------------- | ------------------------------------------------------------ |
| ROS2              | Middleware that coordinates communication between components |
| Gazebo            | Physics simulation and visualization                         |
| Betaflight SITL   | Flight controller running in simulation                      |
| Python Controller | Autonomous control logic                                     |

High-level pipeline:

Gazebo (physics simulation)
⬇
Drone dynamics + sensors
⬇
Betaflight SITL (flight controller)
⬇
MAVLink messages
⬇
ROS2 bridge
⬇
Python autonomous controller

---

# Technology Stack

## ROS2

This project uses **ROS2 Humble** as the main communication layer. ROS2 allows different processes to exchange messages and control the drone in a modular way.

ROS2 is responsible for:

* coordinating the simulation components
* providing topics/services for control
* connecting the Python controller with the simulator

---

## Gazebo

**Gazebo** provides the physics simulation of the drone and the environment.

Gazebo simulates:

* rigid body physics
* propeller thrust
* gravity and collisions
* drone pose and velocity

The simulated drone publishes its state to ROS2.

---

## Betaflight SITL

**Betaflight SITL (Software-In-The-Loop)** runs the real Betaflight firmware as a simulated flight controller.

It performs the same tasks as a real flight controller:

* PID stabilization
* motor mixing
* attitude control
* sensor processing

Instead of sending signals to real motors, it communicates through **MAVLink** to the simulator.

---

## MAVLink

**MAVLink** is the communication protocol used between the controller and the drone.

In this project MAVLink is used to send commands such as:

* angular velocities
* roll / pitch / yaw targets
* throttle commands

---

## Python Controller

The autonomous logic is implemented in **Python**.

The controller subscribes to the drone state and publishes MAVLink commands to guide the drone along a trajectory.

Currently implemented behavior:

**Circular trajectory flight**

The drone flies a circle in the air by continuously applying angular motion.

---

# Control Modes

The controller supports multiple control modes.

## Angular Velocity Mode

The drone receives body angular velocity commands.

Example:

* constant yaw rate
* small pitch angle

This causes the drone to move in a circular path.

---

## RPY Mode (Roll / Pitch / Yaw)

Instead of angular velocities, the controller sends:

* Roll
* Pitch
* Yaw
* Throttle

By adjusting roll and yaw over time, the drone can follow the circular trajectory.

---

# Configuration

The control mode can be configured in the controller settings:

```
control_mode = "angular_velocity"
```

or

```
control_mode = "rpy"
```

Other configurable parameters include:

* circle radius
* angular speed
* altitude
* control frequency

---

# How It Works

1. Gazebo starts the drone simulation.
2. Betaflight SITL runs the drone flight controller.
3. MAVLink connects the controller to the drone.
4. ROS2 acts as the communication layer.
5. The Python controller computes control commands.
6. Commands are sent to the drone.
7. The drone stabilizes itself using Betaflight and follows the trajectory.

The result is a fully simulated autonomous drone performing controlled motion.

---

# Future Work

Possible improvements:

* waypoint navigation
* trajectory planning
* vision-based navigation
* reinforcement learning controllers
* real drone deployment

---

# Goal

The long-term goal is to create a modular environment for testing **autonomous drone algorithms** using a realistic flight controller and physics simulation before deploying on real hardware.

---

# License

MIT License
