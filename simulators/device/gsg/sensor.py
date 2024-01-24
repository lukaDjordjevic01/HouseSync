from .MPU6050 import MPU6050
import time


def run_gsg_loop(device_id, delay, callback, stop_event, publish_event, settings):
    mpu = MPU6050.MPU6050()
    mpu.dmp_initialize()
    while not stop_event.is_set():
        accel = mpu.get_acceleration()  # get accelerometer data
        gyro = mpu.get_rotation()  # get gyroscope data

        acceleration = [accel[0] / 16384.0, accel[1] / 16384.0, accel[2] / 16384.0]
        rotation = [gyro[0] / 131.0, gyro[1] / 131.0, gyro[2] / 131.0]

        callback(device_id, acceleration, rotation, publish_event, settings)
        time.sleep(delay)


