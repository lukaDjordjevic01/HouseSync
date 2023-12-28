import math
import time


def run_gsg_simulator(device_id, delay, callback, stop_event, publish_event, settings):
    time_step = 0.1  # Time step for simulation
    time_elapsed = 0.0  # Initialize time elapsed

    while not stop_event.is_set():
        # Simulate acceleration values (sine function for periodic motion)
        accel_x = 0.5 * math.sin(2 * math.pi * time_elapsed)
        accel_y = 0.7 * math.sin(1.5 * math.pi * time_elapsed)
        accel_z = 0.3 * math.sin(math.pi * time_elapsed)

        # Simulate rotation values (cosine function for periodic motion)
        gyro_x = 50.0 * math.cos(2 * math.pi * time_elapsed)
        gyro_y = 30.0 * math.cos(1.5 * math.pi * time_elapsed)
        gyro_z = 20.0 * math.cos(math.pi * time_elapsed)

        acceleration = [accel_x, accel_y, accel_z]
        rotation = [gyro_x, gyro_y, gyro_z]

        callback(device_id, acceleration, rotation, publish_event, settings)
        time.sleep(delay)

        time_elapsed += time_step
