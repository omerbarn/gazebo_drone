import time
import math
from pymavlink import mavutil

class DroneManager:
    """
    Low-level class to manage MAVLink communication with ArduPilot.
    """
    def __init__(self, connection_string):
        print(f"Connecting to drone at {connection_string}...")
        self.master = mavutil.mavlink_connection(connection_string)
        self.wait_for_heartbeat()
        self.boot_time = time.time()

    def wait_for_heartbeat(self):
        print("Waiting for heartbeat...")
        self.master.wait_heartbeat()
        print(f"Heartbeat from system (system {self.master.target_system} component {self.master.target_component})")

    def set_mode(self, mode):
        print(f"Setting mode to {mode}...")
        if mode not in self.master.mode_mapping():
            print(f"Unknown mode : {mode}")
            return False
        mode_id = self.master.mode_mapping()[mode]
        self.master.mav.set_mode_send(
            self.master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id
        )
        return True

    def arm(self):
        print("Arming...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0
        )
        self.master.motors_armed_wait()
        print("Armed!")

    def disarm(self):
        print("Disarming...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        self.master.motors_disarmed_wait()
        print("Disarmed!")

    def takeoff(self, altitude):
        print(f"Taking off to {altitude}m...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0, 0, 0, altitude
        )

    def set_rc(self, channel, pwm):
        """
        Send RC_CHANNELS_OVERRIDE for a specific channel.
        """
        rc_values = [65535] * 18 # 65535 means no change
        rc_values[channel - 1] = pwm
        self.master.mav.rc_channels_override_send(
            self.master.target_system,
            self.master.target_component,
            *rc_values
        )

    def set_attitude(self, roll=0, pitch=0, yaw=0, thrust=0.5):
        """
        Send SET_ATTITUDE_TARGET.
        roll, pitch, yaw in degrees. thrust 0 to 1.
        """
        def euler_to_quaternion(r, p, y):
            r = math.radians(r)
            p = math.radians(p)
            y = math.radians(y)
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

        q = euler_to_quaternion(roll, pitch, yaw)
        self.master.mav.set_attitude_target_send(
            int(1e3 * (time.time() - self.boot_time)),
            self.master.target_system,
            self.master.target_component,
            0b00000111, # Ignore attitude rates
            q,
            0, 0, 0, # body rates
            thrust
        )

    def set_angular_acceleration(self, roll_accel=0, pitch_accel=0, yaw_accel=0, thrust=0.5):
        """
        Simulate setting angular acceleration using attitude rates or similar.
        Note: Direct angular acceleration is not always available via standard MAVLink messages
        without specialized firmware or messages. We use rate targets as a proxy.
        """
        self.master.mav.set_attitude_target_send(
            int(1e3 * (time.time() - self.boot_time)),
            self.master.target_system,
            self.master.target_component,
            0b10000000, # Ignore attitude quaternion, use rates
            [1, 0, 0, 0],
            roll_accel, pitch_accel, yaw_accel,
            thrust
        )

    def get_mode(self):
        msg = self.master.recv_match(type='HEARTBEAT', blocking=True)
        mode = mavutil.mode_string_v10(msg)
        return mode

class MissionController:
    """
    High-level class for flight logic.
    """
    def __init__(self, drone_manager):
        self.drone = drone_manager

    def execute_circle_mission(self):
        print("Starting Circle Mission...")
        self.drone.set_mode('GUIDED')
        self.drone.arm()
        self.drone.takeoff(10)

        # Wait for takeoff to reach altitude
        time.sleep(10)

        print("Beginning circle trajectory...")
        start_time = time.time()
        while time.time() - start_time < 30:
            # Use RPY to move in a circle
            self.drone.set_attitude(roll=5, pitch=5, yaw=0, thrust=0.6)
            time.sleep(0.1)

        print("Returning to Launch...")
        self.drone.set_mode('RTL')

    def execute_manual_drive(self):
        print("Starting Manual Drive Test...")
        self.drone.set_mode('STABILIZE')
        self.drone.arm()

        # Test RC override for throttle
        print("Throttle up...")
        for i in range(1100, 1600, 10):
            self.drone.set_rc(3, i)
            time.sleep(0.1)

        time.sleep(5)

        print("Throttle down...")
        for i in range(1600, 1000, -10):
            self.drone.set_rc(3, i)
            time.sleep(0.1)

        self.drone.disarm()

if __name__ == "__main__":
    # Use UDP port matching ArduPilot SITL's default (e.g. 14550 or 14551)
    # Inside docker-compose we'll point to the SITL container
    manager = DroneManager('udp:127.0.0.1:14550')
    mission = MissionController(manager)

    # Choose a mission
    # mission.execute_circle_mission()
    mission.execute_manual_drive()
