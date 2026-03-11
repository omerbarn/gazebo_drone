import time
import math
from pymavlink import mavutil

def connect_to_drone():
    print("Waiting for Betaflight SITL...")
    # Betaflight SITL usually listens on TCP 5761 for UART1 by default in SITL
    # Since we set network_mode: host, we connect to localhost:5761
    connection = mavutil.mavlink_connection('tcp:127.0.0.1:5761')
    while True:
        try:
            connection.wait_heartbeat(timeout=5)
            print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))
            break
        except Exception:
            print("Waiting for heartbeat on tcp:127.0.0.1:5761...")
    return connection

def arm_drone(master):
    print("Arming...")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 0, 0, 0, 0, 0, 0)

    # Wait for arming (Betaflight might take a second)
    time.sleep(2)
    print("Armed (hopefully)!")

def euler_to_quaternion(r, p, y):
    cr = math.cos(r * 0.5)
    sr = math.sin(r * 0.5)
    cp = math.cos(p * 0.5)
    sp = math.sin(p * 0.5)
    cy = math.cos(y * 0.5)
    sy = math.sin(y * 0.5)
    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    return [qw, qx, qy, qz]

def send_attitude_target(master, roll=0.0, pitch=0.0, yaw_rate=0.0, thrust=0.5):
    """
    roll, pitch are in radians
    thrust is 0 to 1
    """
    q = euler_to_quaternion(roll, pitch, 0)

    master.mav.set_attitude_target_send(
        int(1e3 * time.time()), # time_boot_ms
        master.target_system,
        master.target_component,
        0b00000111, # type_mask: use attitude quaternion (bits 0,1,2 ignore rates)
        q,
        0, 0, yaw_rate, # body rates
        thrust
    )

def takeoff(master):
    print("Taking off...")
    # Gradually increase thrust
    for i in range(100):
        send_attitude_target(master, thrust=0.4 + (i * 0.002))
        time.sleep(0.05)
    print("Climbing...")
    for _ in range(100):
        send_attitude_target(master, thrust=0.6)
        time.sleep(0.05)

def circular_flight(master, duration=60):
    print("Executing circular trajectory...")
    start_time = time.time()

    while time.time() - start_time < duration:
        # Fly in a circle: small inward roll + small forward pitch + constant yaw rate
        send_attitude_target(master, roll=0.1, pitch=0.05, yaw_rate=0.4, thrust=0.55)
        time.sleep(0.05)

    print("Circular flight done!")

def land(master):
    print("Landing...")
    for i in range(200):
        send_attitude_target(master, thrust=0.5 - (i * 0.002))
        time.sleep(0.05)
    # Disarm
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        0, 0, 0, 0, 0, 0, 0)
    print("Landed and Disarmed.")

if __name__ == "__main__":
    try:
        master = connect_to_drone()
        arm_drone(master)
        takeoff(master)
        circular_flight(master, 60)
        land(master)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
