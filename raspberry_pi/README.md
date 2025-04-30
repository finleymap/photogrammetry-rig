# Raspberry Pi Photogrammetry Rig Scripts

This folder contains Python scripts designed to run on a Raspberry Pi-based photogrammetry rig. The setup automates image capture and mask generation for 3D reconstruction workflows.

---

## Scripts Included

### 1. `capture_images.py`
This script:
- Controls two stepper motors (vertical and rotational axes).
- Captures images using the Raspberry Pi camera at three vertical positions.
- Automatically names and saves images into `~/final_output/images/`.

#### Key Features:
- Uses `libcamera-still` for high-resolution image capture.
- Uses a limit switch to establish a repeatable home position.
- Accepts number of turntable positions as a command-line argument (e.g., 40 for 9° increments).

---

### 2. `generate_masks.py`
This script:
- Processes all images in `~/final_output/images/`.
- Removes the background using the `rembg` library.
- Converts the alpha channel to a binary mask and applies dilation.
- Saves the masks in `~/final_output/masks/`.

---

## Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
