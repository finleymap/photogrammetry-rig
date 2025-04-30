import pigpio
import time
import os
import subprocess
from datetime import datetime

# Motor 1 (Positioning) Pins
STEP1 = 17  # GPIO17 (Physical pin 11)
DIR1 = 27   # GPIO27 (Physical pin 13)

# Motor 2 (Rotation) Pins
STEP2 = 23  # GPIO23 (Physical pin 16)
DIR2 = 24   # GPIO24 (Physical pin 18)

# Limit Switch
LIMIT_SWITCH_PIN = 25  # GPIO25 (Physical pin 22)

# Constants
STEPS_PER_REV = 800
STEP_DELAY_US = 2000  # microseconds
INITIAL_OFFSET = int(1.25 * STEPS_PER_REV)        # 1000 steps
STEP_BETWEEN_POSITIONS = int(1.0 * STEPS_PER_REV / 2)  # 400 steps

# Output Folder
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
save_folder = os.path.expanduser(f"~/Pictures/photogrammetry_{timestamp}")
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

# ===== Safety & Motion Helpers =====
def check_emergency_stop():
    if pi.read(LIMIT_SWITCH_PIN) == 0:
        raise Exception("Emergency stop triggered: limit switch pressed unexpectedly!")

def step_motor(step_pin, dir_pin, steps, direction, delay_us):
    pi.write(dir_pin, direction)
    for _ in range(steps):
        check_emergency_stop()
        pi.write(step_pin, 1)
        time.sleep(delay_us / 1_000_000)
        pi.write(step_pin, 0)
        time.sleep(delay_us / 1_000_000)

def rotate_motor2_with_stops(num_stops, position_index):
    steps_per_segment = STEPS_PER_REV // num_stops
    print(f"🔄 Rotating Motor 2: 360° with {num_stops} stops...")

    for i in range(num_stops):
        print(f" 📸 Segment {i + 1} of {num_stops} — capturing image")

        # Step Motor 2
        step_motor(STEP2, DIR2, steps_per_segment, direction=1, delay_us=STEP_DELAY_US)

        # File name: pos1_img01.jpg, etc.
        image_name = f"pos{position_index}_img{str(i + 1).zfill(2)}.jpg"
        image_path = os.path.join(save_folder, image_name)

        # Capture Image       
        print(f"Capturing: {image_name} - 12MP")
        try:
            subprocess.run([
                "libcamera-still",
                "--width", "4056",
                "--height", "3040",
                "--shutter", "33333",      # ~1/30s
                "--gain", "4",             # Approx ISO 400
                "--lens-position", "9",
                "--nopreview",
                "-o", image_path
            ], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Camera capture failed at segment {i + 1}: {e}")

        # Pause after each capture
        time.sleep(0.5)

    print("Motor 2 full rotation and capture complete.\n")

# ===== Main Sequence =====
try:
    print("🏁 Homing Motor 1 (toward limit switch)...")
    pi.write(DIR1, 1)
    while pi.read(LIMIT_SWITCH_PIN) != 0:
        pi.write(STEP1, 1)
        time.sleep(STEP_DELAY_US / 1_000_000)
        pi.write(STEP1, 0)
        time.sleep(STEP_DELAY_US / 1_000_000)

    print("Limit switch reached — position set to 0 (datum)")
    time.sleep(0.5)

    print("⬅️ Backing off limit switch until released...")
    pi.write(DIR1, 0)
    while pi.read(LIMIT_SWITCH_PIN) == 0:
        pi.write(STEP1, 1)
        time.sleep(STEP_DELAY_US / 1_000_000)
        pi.write(STEP1, 0)
        time.sleep(STEP_DELAY_US / 1_000_000)

    print("Limit switch released.")
    time.sleep(0.5)

    # Move to Position 1 (1000 steps)
    print("➡️ Moving Motor 1 to Position 1 (1000 steps)...")
    step_motor(STEP1, DIR1, INITIAL_OFFSET, direction=0, delay_us=STEP_DELAY_US)

    print("⏸ Pausing before Motor 2 rotation...")
    time.sleep(1)

    print("🔄 Running Motor 2 at Position 1...")
    rotate_motor2_with_stops(num_stops=30, position_index=1)

    # Move to Position 2 and 3
    for pos in range(2, 4):
        print(f"➡️ Moving Motor 1 to Position {pos} ({STEP_BETWEEN_POSITIONS} steps)...")
        step_motor(STEP1, DIR1, STEP_BETWEEN_POSITIONS, direction=1, delay_us=STEP_DELAY_US)

        print("⏸ Pausing before Motor 2 rotation...")
        time.sleep(0.5)

        print(f"🔄 Running Motor 2 at Position {pos}...")
        rotate_motor2_with_stops(num_stops=30, position_index=pos)

    print("Sequence complete. All images captured.")

except KeyboardInterrupt:
    print("Stopped by user.")

except Exception as e:
    print(f"Emergency Halt: {e}")

finally:
    pi.stop()
