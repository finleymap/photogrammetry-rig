import pigpio
import time
import os
import subprocess
from datetime import datetime

# Motor 2 (Turntable) Pins
STEP_PIN = 23  # GPIO23 (Physical pin 16)
DIR_PIN = 24   # GPIO24 (Physical pin 18)

# Constants
STEPS_PER_REV = 800
NUM_POSITIONS = 40
STEP_DELAY_US = 2000  # microseconds

# Output Folder
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
save_folder = os.path.expanduser(f"~/Pictures/turntable_capture_{timestamp}")
os.makedirs(save_folder, exist_ok=True)

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon.")
    exit()

# Setup GPIO
pi.set_mode(STEP_PIN, pigpio.OUTPUT)
pi.set_mode(DIR_PIN, pigpio.OUTPUT)

def step_motor(steps, direction, delay_us):
    pi.write(DIR_PIN, direction)
    for _ in range(steps):
        pi.write(STEP_PIN, 1)
        time.sleep(delay_us / 1_000_000)
        pi.write(STEP_PIN, 0)
        time.sleep(delay_us / 1_000_000)

# Calculate steps per increment
steps_per_increment = STEPS_PER_REV / NUM_POSITIONS
accumulated_error = 0.0

# Main Loop
try:
    for index in range(1, NUM_POSITIONS + 1):
        base_name = f"image_{str(index).zfill(3)}"
        filepath_12mp = os.path.join(save_folder, f"{base_name}_12MP.jpg")

        print(f"📸 Capturing: {base_name} - 12MP")
        subprocess.run([
            "libcamera-still",
            "--width", "4056",
            "--height", "3040",
            "--shutter", "33333",      # ~1/17s
            "--gain", "4",           # Approx ISO 400
            "--lens-position", "9",
            "--nopreview",             # 🔇 No preview window
            "-o", filepath_12mp
        ], check=True)

        # Add EXIF metadata for 12MP image
        subprocess.run([
            "exiftool",
            "-Make=Raspberry Pi",
            "-Model=ov64a40",
            "-Software=rpicam-apps",
            "-ExposureTime=1/33",
            "-ISO=337",
            "-SubjectDistance=0.1667",
            "-overwrite_original",
            filepath_12mp
        ], check=True)

        # Rotate turntable to next position
        if index < NUM_POSITIONS:
            accumulated_error += steps_per_increment
            rounded_steps = int(accumulated_error)
            accumulated_error -= rounded_steps
            step_motor(rounded_steps, direction=1, delay_us=STEP_DELAY_US)

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")

finally:
    pi.stop()
    print("🔌 GPIO released. Bye!")
