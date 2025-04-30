# User Computer Scripts for Photogrammetry Workflow

This folder contains Python scripts that run on your host computer (e.g., laptop or desktop) and manage the full photogrammetry process using a Raspberry Pi rig and Meshroom.

---

## Scripts Overview

### `automate.py`

This script automates the entire photogrammetry pipeline by:
- Connecting to a Raspberry Pi via SSH
- Running two remote scripts:
  - `capture_images.py` (image acquisition)
  - `generate_masks.py` (background removal and mask generation)
- Downloading the image/mask output from the Pi
- Launching Meshroom in batch mode to process images up to `StructureFromMotion`
- Opening the resulting project in Meshroom GUI

#### User Configuration
Edit the following variables in the script to match your setup:

```python
pi_user = "pi_username"          # Your Raspberry Pi username
pi_host = "192.168.x.x"          # IP address of the Pi
remote_scripts_path = "/home/pi_username/scripts"  # Path on the Pi

meshroom_batch_path = r"C:\\Path\\To\\Meshroom\\meshroom_batch.exe"
meshroom_gui_path = r"C:\\Path\\To\\Meshroom\\meshroom.exe"
```

#### How to Use
```bash
python automate.py
```

---

### `calibration.py`

This script performs **intrinsic camera calibration** using chessboard images stored locally.

#### What It Does
- Searches for calibration images in the `calibration_images/` folder.
- Detects a 4×5 chessboard pattern (can be adjusted).
- Computes camera intrinsics and distortion coefficients.
- Saves:
  - `camera_matrix.txt`
  - `distortion_coefficients.txt`
  - Annotated checkerboard images in `output/`
  - A `calibration_report.txt` with reprojection error

#### User Configuration
- **CHESSBOARD_SIZE**: Update this if your calibration board has a different number of inner corners.
- **SQUARE_SIZE**: Update if your checkerboard square size is not 2 cm.
- **CALIBRATION_IMAGES_PATH**: Ensure images are placed in `calibration_images/`.

#### Example Usage
```bash
python calibration.py
```

---

## Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**
```
numpy
opencv-python
```

> `automate.py` uses only Python’s built-in standard libraries.

---

## Output Structure

After running the pipeline, you will have:

```
~/final_output/
├── images/     # Captured photos
├── masks/      # Generated masks
└── project.mg  # Meshroom project
```

Calibration output will be saved to:

```
output/
├── corners_*.jpg
├── camera_matrix.txt
├── distortion_coefficients.txt
└── calibration_report.txt
```

---

## Notes

- Make sure SSH access is set up between your computer and the Raspberry Pi.
- Meshroom must be installed, and executable paths must be correctly set in `automate.py`.

---

## License

MIT License — free to use and modify with attribution.

