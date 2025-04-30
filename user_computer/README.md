# User Computer Scripts for Photogrammetry Workflow

This folder contains scripts intended to be run on the **host machine** (e.g. your laptop or desktop) that interfaces with the Raspberry Pi photogrammetry rig. These tools manage the end-to-end process of capturing images, generating masks, downloading data, and performing structure-from-motion (SfM) reconstruction using Meshroom.

---

## Scripts Overview

### 1. `automate.py`

This is the main automation script. It remotely runs photogrammetry routines on the Raspberry Pi, downloads the output, and kicks off a Meshroom reconstruction pipeline.

#### What It Does:
- Prompts the user for the number of rotational positions.
- Connects to the Raspberry Pi via SSH and runs:
  - `capture_images.py` (image capture script on Pi)
  - `generate_masks.py` (background removal and mask generation)
- Downloads the `~/final_output` folder from the Pi.
- Runs Meshroom in batch mode to compute up to the `StructureFromMotion` node.
- Opens the resulting `.mg` project in the Meshroom GUI.

#### User Configuration Required:
You **must update** the following variables at the top of the script:
- `pi_user` – your Raspberry Pi username (usually `"pi"`)
- `pi_host` – the IP address of your Raspberry Pi on your network
- `remote_scripts_path` – the full path to where the Pi scripts are stored (e.g. `/home/pi/scripts`)
- `meshroom_batch_path` – full path to `meshroom_batch.exe` on your local machine
- `meshroom_gui_path` – full path to `meshroom.exe` on your local machine

#### Example:
```bash
python automate.py

