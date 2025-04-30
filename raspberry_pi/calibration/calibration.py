import numpy as np
import cv2
import glob
import os

# === Config ===
CHESSBOARD_SIZE = (4, 5)  # (inner corners per row, column)
SQUARE_SIZE = 2  # in centimeters
CALIBRATION_IMAGES_PATH = 'calibration_images/*.jpg'
OUTPUT_DIRECTORY = 'output'

def calibrate_camera():
    # Prepare object points based on real-world coordinates
    objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)
    objp *= SQUARE_SIZE

    objpoints = []
    imgpoints = []

    images = glob.glob(CALIBRATION_IMAGES_PATH)

    if not images:
        print(f"No images found at: {CALIBRATION_IMAGES_PATH}")
        return

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    print(f"Found {len(images)} images")

    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

        if ret:
            objpoints.append(objp)

            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            cv2.drawChessboardCorners(img, CHESSBOARD_SIZE, corners2, ret)

            out_path = os.path.join(OUTPUT_DIRECTORY, f'corners_{os.path.basename(fname)}')
            cv2.imwrite(out_path, img)
            print(f"{fname}: Checkerboard found → saved corners image")
        else:
            print(f"{fname}: Checkerboard NOT found")

    if not objpoints:
        print("No checkerboards were detected. Exiting.")
        return

    print("Calibrating camera...")

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Save as text files
    np.savetxt(os.path.join(OUTPUT_DIRECTORY, 'camera_matrix.txt'), mtx, fmt='%.6f')
    np.savetxt(os.path.join(OUTPUT_DIRECTORY, 'distortion_coefficients.txt'), dist, fmt='%.6f')

    with open(os.path.join(OUTPUT_DIRECTORY, 'calibration_report.txt'), 'w') as f:
        f.write(f"Reprojection Error (RMS): {ret:.6f}\n")

    print("Calibration complete!")
    print(f"Results saved to: {OUTPUT_DIRECTORY}")

if __name__ == "__main__":
    calibrate_camera()
