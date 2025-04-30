import pigpio
import time
import os
import subprocess
import sys

# Motor 1 (Z-axis positioning) Pins
STEP1 = 17  # GPIO17
DIR1 = 27   # GPIO27

# Motor 2 (Turntable) Pins
STEP2 = 23  # GPIO23
DIR2 = 24   # GPIO24

# Limit Switch Pin
LIMIT_SWITCH_PIN = 25  # GPIO25

# Constants
STEPS_PER_REV = 800
STEP_DELAY_US = 2000  # microseconds
INITIAL_OFFSET = int(1.25 * STEPS_PER_REV)        # 1000 steps up
STEP_BETWEEN_POSITIONS = int(1.0 * STEPS_PER_REV / 2)  # 400 steps

# Get number of turntable positions from command-line argument
try:
    num_stops = int(sys.argv[1])
    if num_stops <= 0 or num_stops > STEPS_PER_REV:
        raise ValueError
except (IndexError, ValueError):
    print("Usage: python script.py <number_of_images>")
    print("Please enter a valid number of images (1 to 800).")
    exit()

# Output Folder (user-independent)
save_folder = os.path.join(os.path.expanduser("~"), "final_output", "images")
os.makedirs(save_folder, exist_ok=True)

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon.")
    exit()

# Setup GPIO
for pin in [STEP1, DIR1, STEP2, DIR2]:
    pi.set_mode(pin, pigpio.OUTPUT)
pi.set_mode(LIMIT_SWITCH_PIN, pigpio.INPUT)
pi.set_pull_up_down(LIMIT_SWITCH_PIN, pigpio.PUD_UP)

# Safety check
def check_emergency_stop():
    if pi.read(LIMIT_SWITCH_PIN) == 0:
        raise Exception("Emergency stop triggered: limit switch pressed unexpectedly!")

# General step function
def step_motor(step_pin, dir_pin, steps, direction, delay_us):
    pi.write(dir_pin, direction)
    for _ in range(steps):
        check_emergency_stop()
        pi.write(step_pin, 1)
        time.sleep(delay_us / 1_000_000)
        pi.write(step_pin, 0)
        time.sleep(delay_us / 1_000_000)

# Turntable rotation with error correction
def rotate_motor2_with_stops(num_stops, position_index):
    steps_per_increment = STEPS_PER_REV / num_stops
    accumulated_error = 0.0

    print(f"Rotating Motor 2: 360° with {num_stops} positions...")

    for i in range(num_stops):
        print(f"Capturing image {i + 1} of {num_stops}")

        # File name
        image_name = f"pos{position_index}_img{str(i + 1).zfill(2)}.jpg"
        image_path = os.path.join(save_folder, image_name)

        # Capture image
        try:
            subprocess.run([
                "libcamera-still",
                "--width", "4056",
                "--height", "3040",
                "--shutter", "33333",
                "--gain", "4",
                "--lens-position", "9",
                "--nopreview",
                "-o", image_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Camera capture failed at segment {i + 1}: {e}")

        # Calculate and apply rotation
        if i < num_stops - 1:
            accumulated_error += steps_per_increment
            steps = int(accumulated_error)
            accumulated_error -= steps
            step_motor(STEP2, DIR2, steps, direction=1, delay_us=STEP_DELAY_US)

    print("Rotation complete.")

# Main operation
try:
    print("Homing Motor 1 (toward limit switch)...")
    pi.write(DIR1, 1)
    while pi.read(LIMIT_SWITCH_PIN) != 0:
        pi.write(STEP1, 1)
        time.sleep(STEP_DELAY_US / 1_000_000)
        pi.write(STEP1, 0)
        time.sleep(STEP_DELAY_US / 1_000_000)

    print("Limit switch reached. Datum established.")
    time.sleep(0.5)

    print("Backing off limit switch...")
    pi.write(DIR1, 0)
    while pi.read(LIMIT_SWITCH_PIN) == 0:
        pi.write(STEP1, 1)
        time.sleep(STEP_DELAY_US / 1_000_000)
        pi.write(STEP1, 0)
        time.sleep(STEP_DELAY_US / 1_000_000)

    time.sleep(0.5)

    print("Moving to Position 1...")
    step_motor(STEP1, DIR1, INITIAL_OFFSET, direction=0, delay_us=STEP_DELAY_US)
    time.sleep(1)

    print("Capturing at Position 1...")
    rotate_motor2_with_stops(num_stops=num_stops, position_index=1)

    for pos in range(2, 4):
        print(f"Moving to Position {pos}...")
        step_motor(STEP1, DIR1, STEP_BETWEEN_POSITIONS, direction=1, delay_us=STEP_DELAY_US)
        time.sleep(0.5)
        print(f"Capturing at Position {pos}...")
        rotate_motor2_with_stops(num_stops=num_stops, position_index=pos)

    print("All captures completed.")

except KeyboardInterrupt:
    print("Capture interrupted by user.")

except Exception as e:
    print(f"Emergency Halt: {e}")

finally:
    pi.stop()
