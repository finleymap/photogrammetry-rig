import os
import io
import cv2
import numpy as np
from PIL import Image
from rembg import remove

# Input/output paths using current user's home directory
base_folder = os.path.join(os.path.expanduser("~"), "final_output")
input_folder = os.path.join(base_folder, "images")
output_folder = os.path.join(base_folder, "masks")
os.makedirs(output_folder, exist_ok=True)

dilation_radius = 5

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_filename = base_name + ".png"
        output_path = os.path.join(output_folder, output_filename)

        print(f"Processing: {filename}")

        # Step 1: Remove background
        with open(input_path, 'rb') as f:
            output_bytes = remove(f.read())

        # Step 2: Create mask from alpha channel
        img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
        alpha = img.split()[-1]
        mask = alpha.point(lambda p: 255 if p > 0 else 0).convert("L")

        # Step 3: Dilate mask
        mask_array = np.array(mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation_radius, dilation_radius))
        dilated = cv2.dilate(mask_array, kernel, iterations=1)

        # Step 4: Save mask
        final_mask = Image.fromarray(dilated)
        final_mask.save(output_path)

        print(f"Saved mask: {output_path}")
