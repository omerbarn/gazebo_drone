import time
import math
from pymavlink import mavutil

# Betaflight RC Channel mapping (standard)
# CH1: Roll, CH2: Pitch, CH3: Throttle, CH4: Yaw
# AUX1: Arm (usually)

def connect_to_drone():
    print("Waiting for Betaflight SITL...")
    connection = mavutil.mavlink_connection('tcp:127.0.0.1:5761')
    while True:
        try:
            connection.wait_heartbeat(timeout=5)
            print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))
            break
        except Exception:
            print("Waiting for heartbeat on tcp:127.0.0.1:5761...")
    return connection

def set_rc(master, roll=1500, pitch=1500, throttle=1000, yaw=1500, aux1=1000):
    """
    Send RC_CHANNELS_OVERRIDE
    Values should be between 1000 and 2000
    """
    # CH1-CH8
    channels = [roll, pitch, throttle, yaw, aux1, 0, 0, 0]
    master.mav.rc_channels_override_send(
        master.target_system,
        master.target_component,
        *channels
    )

def arm_drone(master):
    print("Arming via AUX1...")
    # Betaflight often uses a specific channel for arming
    # Let's send AUX1 high (2000) to arm
    for _ in range(10):
        set_rc(master, aux1=2000)
        time.sleep(0.1)
    print("Armed (AUX1 high)")

def takeoff(master):
    print("Taking off (increasing throttle)...")
    for i in range(100):
        # Gradually increase throttle from 1000 to 1600
        throttle = 1000 + (i * 6)
        set_rc(master, throttle=throttle, aux1=2000)
        time.sleep(0.05)
    print("Climbing...")
    for _ in range(40):
        set_rc(master, throttle=1600, aux1=2000)
        time.sleep(0.05)

def circular_flight(master, duration=60):
    print("Executing circular trajectory via RC...")
    start_time = time.time()
    while time.time() - start_time < duration:
        # Roll 1600 (right), Pitch 1550 (forward), Yaw 1550 (right turn)
        set_rc(master, roll=1600, pitch=1550, throttle=1550, yaw=1550, aux1=2000)
        time.sleep(0.05)
    print("Circular flight done!")

def land(master):
    print("Landing...")
    for i in range(100):
        throttle = 1550 - (i * 5)
        set_rc(master, throttle=max(1000, throttle), aux1=2000)
        time.sleep(0.05)
    # Disarm
    set_rc(master, aux1=1000)
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
        # Try to disarm
        if 'master' in locals():
            set_rc(master, aux1=1000)
    except Exception as e:
        print(f"Error: {e}")
