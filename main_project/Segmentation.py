# segmentation.py
import cv2
import os

def segment_image_into_6_parts(image_path, output_folder="parts"):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    h, w = img.shape[:2]
    os.makedirs(output_folder, exist_ok=True)

    # Divide height into 6 equal parts
    part_height = h // 6

    for i in range(6):
        y_start = i * part_height
        y_end = (i + 1) * part_height if i < 5 else h  # Last part takes remainder
        part = img[y_start:y_end, :]  # Full width

        part_path = f"{output_folder}/part_{i+1}.jpg"
        cv2.imwrite(part_path, part)
        print(f"✅ Saved: {part_path}")

    print(f"📐 Image split into 6 parts (each ~{part_height}px tall)")

if __name__ == "__main__":
    segment_image_into_6_parts("preprocessed.jpg", "parts")