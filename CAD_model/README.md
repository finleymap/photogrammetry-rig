## Photogrammetry Rig – 3D CAD Model and Assembly Notes

This repository includes a complete 3D model of the photogrammetry rig used for automated image capture, exported in the neutral `.STEP` format for compatibility with most CAD platforms.

---

### File Overview

- **File:** `photogrammetry_rig.step`
- **Format:** STEP AP214 (.step)
- **Source:** Modeled in SolidWorks, exported for cross-platform access
- **Scale:** 1:1 in millimeters
---

### Physical Setup Instructions

To build the physical rig based on this model, you will need:

#### Hardware:
- **Brass heat-set inserts** (press-fit into 3D-printed parts using a soldering iron)
- **Bolts and screws:**
  - M2 bolts (for camera mounting)
  - M3 bolts (for most structural parts)
  - M5 bolts (for frame or large-load joints)

#### Electronics:
- **Camera:** Connect to the Raspberry Pi using the **CSI ribbon cable** and plug into the **CSI port** on the Pi (located near the HDMI ports).
- **Limit switch:** Should be positioned as shown in the model to establish the Z-axis home position.
- **Motors:** NEMA 17 or similar stepper motors, depending on your design.

---

###  Included Components
This model includes:
- Camera bracket
- Stepper motor mounts (turntable and vertical axis)
- Base frame and guides

---
