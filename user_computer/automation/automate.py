import subprocess
import os
import sys
import time

# === CONFIG ===
pi_user = "pi_username"  # Replace with your Pi's username
pi_host = "192.168.x.x"  # Replace with your Pi's IP address
remote_scripts_path = "/home/pi_username/scripts"  # Update if needed

# Remote and local paths
remote_output_path = "/home/pi_username/final_output"
local_save_path = os.path.abspath(os.path.join(os.path.expanduser("~"), "final_output"))
images_path = os.path.join(local_save_path, "images")
masks_path = os.path.join(local_save_path, "masks")

# Meshroom paths (update for your Windows system)
meshroom_batch_path = r"C:\Path\To\Meshroom\meshroom_batch.exe"
meshroom_gui_path = r"C:\Path\To\Meshroom\meshroom.exe"
project_file_path = os.path.abspath(os.path.join(local_save_path, "project.mg"))

# === Ask how many photos to take ===
num_photos = input("How many photos would you like to capture? ")

# Start overall timer
overall_start = time.time()

# === Step 1: Run capture_images.py on Raspberry Pi ===
print(f"\nCapturing {num_photos} photos on Raspberry Pi...")
capture_start = time.time()
subprocess.run([
    "ssh", f"{pi_user}@{pi_host}",
    f"source ~/venvs/turntable-env/bin/activate && {remote_scripts_path}/capture_images.py {num_photos}"
], check=True)
capture_end = time.time()

# === Step 2: Run generate_masks.py on Raspberry Pi ===
print("\nGenerating masks on Raspberry Pi...")
masks_start = time.time()
subprocess.run([
    "ssh", f"{pi_user}@{pi_host}",
    f"source ~/venvs/turntable-env/bin/activate && {remote_scripts_path}/generate_masks.py"
], check=True)
masks_end = time.time()

# === Step 3: Download final_output folder from Pi to local machine ===
print("\nDownloading final output from Raspberry Pi...")
download_start = time.time()
if os.path.exists(local_save_path):
    print("Existing 'final_output' folder found. Removing...")
    subprocess.run(["rm", "-rf", local_save_path])

subprocess.run([
    "scp", "-r",
    f"{pi_user}@{pi_host}:{remote_output_path}",
    local_save_path
], check=True)
download_end = time.time()

# === Step 4: Run Meshroom batch to compute up to SfM ===
print("\nRunning Meshroom batch up to StructureFromMotion...")
meshroom_start = time.time()
subprocess.run([
    meshroom_batch_path,
    "-i", images_path,
    "-o", local_save_path,
    "-p", "photogrammetry",
    "--paramOverrides", "CameraInit:defaultFieldOfView=71.24",
    "--paramOverrides", f'FeatureExtraction:masksFolder={masks_path.replace("\\", "/")}',
    "--compute", "yes",
    "--toNode", "StructureFromMotion",
    "--save", project_file_path
], check=True)
meshroom_end = time.time()

# === Step 5: Open the Meshroom project in GUI ===
print("\nOpening Meshroom GUI with the project...")
time.sleep(2)
subprocess.Popen([meshroom_gui_path, project_file_path])

# Final timing report
overall_end = time.time()

print("\n=== Process Report ===")
print(f"Capture images time: {capture_end - capture_start:.2f} seconds")
print(f"Generate masks time: {masks_end - masks_start:.2f} seconds")
print(f"Download time: {download_end - download_start:.2f} seconds")
print(f"Meshroom compute (CameraInit to SfM) time: {meshroom_end - meshroom_start:.2f} seconds")
print(f"Total process time: {overall_end - overall_start:.2f} seconds")
print("\nAll steps completed successfully.")

