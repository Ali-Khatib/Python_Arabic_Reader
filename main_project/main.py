# main.py
from PreprocessingBGR import crop_image, preprocess_for_arabic_ocr
from Segmentation import segment_image_into_6_parts
from EasyOCRExtraction import extract_from_parts, extract_arabic_text_with_lines
from Config import IMAGE_NAME
import cv2

# Step 1: Preprocess
print("1. Preprocessing...")
body_img = crop_image(IMAGE_NAME)
final_image = preprocess_for_arabic_ocr(body_img)
cv2.imwrite("preprocessed.jpg", final_image)
print("✅ Saved: preprocessed.jpg")

# Step 1.5: Segment into 6 parts
print("1.5. Segmenting into 6 parts...")
segment_image_into_6_parts("preprocessed.jpg", "parts")

# Step 2: OCR from segmented parts
print("2. EasyOCR Extracting text from 6 segmented parts...")
extracted_segmented_text = extract_from_parts("parts")

# Debug: print extracted text
print("\n📝 Extracted Arabic text from  parts:\n")
print(extracted_segmented_text)
print("\n----- End of text extracted from segmentation -----\n")


extracted_text = extract_arabic_text_with_lines("preprocessed.jpg  ")

print("\n📝 Extracted Arabic text from only PP:\n")
print(extracted_text)
print("\n----- End of extracted PP text -----\n")

# Save to file
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(extracted_segmented_text)

print("✅ Done! Text saved to extracted_text.txt")

