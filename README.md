# Photogrammetry Rig Project Repository

This repository contains all components necessary to replicate a low-cost, automated photogrammetry rig for generating accurate 3D models using open-source tools and off-the-shelf hardware.

---

## Included Scripts

### Raspberry Pi Scripts (`raspberry_pi/`)
- **`capture_images.py`**: Captures images at multiple angles using a stepper-motor-controlled turntable and vertical rail. Uses `libcamera-still`.
- **`generate_masks.py`**: Uses `rembg` and `OpenCV` to generate binary masks from captured images.

### User Computer Scripts (`user_computer/`)
- **`automate.py`**: Orchestrates the full process: triggers Raspberry Pi capture, downloads images/masks, runs Meshroom in batch mode, and opens the project.
- **`calibration.py`**: Calibrates the camera using chessboard images and outputs distortion coefficients and camera matrix.

---

## 🛠 CAD Model

Located in `/CAD_model/photogrammetry_rig.step`, this file includes the complete 3D assembly of the rig.

### Setup Notes:
- Uses **brass press-fit inserts** for mounting
- Requires **M2, M3, and M5 bolts** depending on part
- Camera connects via **CSI ribbon cable** to the Raspberry Pi CSI port

---

## Sample Data

Located in `/data/`, this includes:
- A subset of captured images (or a link to OneDrive/Drive)
- Generated masks
- Exported model results (.obj or .glb)

Use this as a reference or baseline to test your own setup.

---

## CCTags Pipeline

Folder `/cctags_pipeline/` includes:
- A **Meshroom pipeline template** configured to use CCTags
- A **CCTags printable marker plate** in PDF format

This enables more real-world scaled models.

---
