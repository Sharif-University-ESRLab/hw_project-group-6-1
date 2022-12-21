import time
import sys
import logging

import numpy as np

import amg8833_i2c
import led

logging.basicConfig(level=logging.INFO, filename='history.log',
                    format='%(asctime)s - %(message)s')

sys.path.append('/')


pin_handler = led.PinHandler()

LEFT = 0
RIGHT = 1
MID = 2

MIN_TEMP = 29
MAX_TEMP = 70
LOGGING_PERIOD = 1 * 60  # Seconds

last_time = None


def generate_submatrices(matrix, sub_size=2):
    submatrices = []
    for i in range(len(matrix) - sub_size + 1):
        for j in range(len(matrix) - sub_size + 1):
            direction = LEFT

            if j == len(matrix) / 2 - 1:
                direction = MID
            elif j >= len(matrix) / 2:
                direction = RIGHT

            submatrices.append(
                (direction, matrix[i:i + sub_size, j:j + sub_size]))

    return submatrices


def log(direction, mean, sub_matrix):
    global last_time

    last_time = time.time()
    logging.info(f"{direction} - {mean} - {sub_matrix}")


def decide_lights(sub_matrices):
    global last_time

    found_left = False
    found_right = False

    for direction, sub_matrix in sub_matrices:
        mean = np.mean(sub_matrix)

        if MIN_TEMP <= mean <= MAX_TEMP:
            if direction == LEFT:
                pin_handler.left_on()
                found_left = True

                if not last_time or time.time() - last_time >= LOGGING_PERIOD:
                    log("LEFT", mean, sub_matrix)

            elif direction == RIGHT:
                pin_handler.right_on()
                found_right = True

                if not last_time or time.time() - last_time >= LOGGING_PERIOD:
                    log("RIGHT", mean, sub_matrix)

            elif direction == MID:
                pin_handler.left_on()
                pin_handler.right_on()
                found_right = True
                found_left = True

                if not last_time or time.time() - last_time >= LOGGING_PERIOD:
                    log("MID", mean, sub_matrix)

    if not found_left:
        pin_handler.left_off()

    if not found_right:
        pin_handler.right_off()

    if not found_left and not found_right:
        last_time = None


def main():

    t0 = time.time()
    sensor = []

    while (time.time() - t0) < 1:
        try:
            sensor = amg8833_i2c.AMG8833(addr=0x69)
        except Exception as e:
            sensor = amg8833_i2c.AMG8833(addr=0x68)
        finally:
            pass

    time.sleep(0.1)

    if not sensor:
        print("No AMG8833 Found - Check Your Wiring")
        sys.exit()

    pixels_resolution = (8, 8)

    pixels_to_read = 64

    while True:
        status, pixels = sensor.read_temp(pixels_to_read)
        if status:
            continue

        T_thermistor = sensor.read_thermistor()

        pixels_reshaped = np.reshape(pixels, pixels_resolution)
        submatrices = generate_submatrices(pixels_reshaped)

        decide_lights(submatrices)
        print(pixels_reshaped)
        print("Thermistor Temperature: {0:2.2f}".format(T_thermistor))


if __name__ == '__main__':
    main()
