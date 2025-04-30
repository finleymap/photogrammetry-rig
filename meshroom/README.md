# CCTag Meshroom Template and Marker Plate

This folder contains a custom Meshroom pipeline template configured for use with CCTag fiducial markers, as well as a printable CCTag marker plate (PDF) for use in structured photogrammetry capture.

---

## Included Files

- `cctag_template.mg`: Meshroom project file pre-configured for CCTag-based SfM pipeline
- `marker_cross_layout.pdf`: Printable plate containing 4 uniquely coded CCTags arranged in a known pattern

---

## Marker Layout and Coordinate System

The marker plate is designed for flat-plane photogrammetry, with the markers arranged symmetrically around the origin.

| Tag ID | Position (mm)  | Notes                 |
|--------|----------------|------------------------|
| 1      | (x=+0.05, z=0)  | Right side of origin   |
| 2      | (x=0, z=+0.05)  | Front of origin        |
| 3      | (x=-0.05, z=0)  | Left side of origin    |
| 4      | (x=0, z=-0.05)  | Back of origin         |

> **Note**: This layout assumes the markers lie on a flat horizontal plane, with **X and Z** axes defining that plane and **Y** as the vertical axis.

---


## Printable Marker Plate

- File: `cctag_plate.pdf`
- Size: Designed to print on A4 or Letter paper
- Tip: Print on matte paper and mount on a rigid flat surface (e.g., foam board)

The tag positions are encoded so Meshroom can reliably determine camera pose when these markers are visible in your scene.

---

## Usage Tips

- Place the marker plate flat and level in your capture area
- Ensure at least **3 markers are visible** in most camera angles
- Keep the plate size to scale with the 0.05 unit spacing (e.g., 50 mm)

---
