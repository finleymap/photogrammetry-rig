# Open-Source Photogrammetry Rig

An open-source, modular photogrammetry system designed to generate accurate 3D reconstructions using affordable, off-the-shelf hardware. This project integrates Raspberry Pi devices, camera calibration methods, and structure-from-motion pipelines to create a reproducible, low-cost solution for 3D capture and reconstruction.

## 📌 Features

- Supports multi-camera rigs using Raspberry Pi boards
- Accurate intrinsic and extrinsic camera calibration using checkerboard patterns
- Automated image capture and storage


## 🛠 Hardware Requirements

- Raspberry Pi 4
- Arducam 64MP or compatible camera modules
- Laser-cut or 3D-printed rig frame


## 📷 Software Stack

- Python (control scripts, camera interface)
- Meshroom open-source 3D Reconstruction Software based on the AliceVision framework.
- `libcamera` for image capture
- `OpenCV` for calibration and image processing
- `Rembg` for masking background removal


## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/finleymap/photogrammetry-rig.git
cd photogrammetry-rig
pip install -r requirements.txt
