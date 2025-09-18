# TessaractExtraction.py
import pytesseract
import cv2
import os
import re

# Configure Tesseract paths
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Users\user\Desktop\Tesseract-OCR\tessdata"

TESSERACT_LANG = "ara"

# ============================
# Helpers
# ============================
def convert_to_arabic_digits(text: str) -> str:
    """Convert Western digits to Arabic-Indic digits"""
    arabic_digits = {
        "0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤",
        "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"
    }
    for en, ar in arabic_digits.items():
        text = text.replace(en, ar)
    return text

def clean_arabic_text(text: str) -> str:
    """Normalize and clean Arabic text"""
    if not text.strip():
        return ""
    text = re.sub(r"\s+", " ", text)  # Fix extra spaces
    text = text.strip()

    # Normalize letters
    replacements = {
        "آ": "ا", "أ": "ا", "إ": "ا",  # Alif
        "ى": "ي", "ئ": "ي", "ؤ": "و", "ة": "ه"  # Yaa, Hamza, Ta
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # Convert digits
    text = convert_to_arabic_digits(text)
    return text

# ============================
# OCR + Segmentation Support
# ============================
def extract_text_with_tesseract(image_path: str) -> str:
    """
    Extract text from a single image using Tesseract
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Cannot load image: {image_path}")
        return ""

    # Run Tesseract (PSM 6: Assume a single uniform block of text)
    raw_text = pytesseract.image_to_string(img, lang=TESSERACT_LANG, config="--psm 6")
    cleaned_lines = [clean_arabic_text(line) for line in raw_text.split("\n") if line.strip()]
    return "\n".join(cleaned_lines)

def tess_extract_from_parts(parts_dir="parts"):
    """
    Extract text from all segmented parts (part_1 to part_6)
    and combine in order.
    """
    all_text = []
    for i in range(1, 5):  # part_1.jpg to part_6.jpg
        part_path = os.path.join(parts_dir, f"part_{i}.jpg")
        if not os.path.exists(part_path):
            print(f"⚠️  Missing: {part_path}")
            continue

        print(f"📄 OCR'ing with Tesseract: {part_path}")
        text = extract_text_with_tesseract(part_path)
        all_text.append(text)

    return "\n".join(all_text)

# ============================
# Run standalone (debug)
# ============================
if __name__ == "__main__":
    if os.path.exists("preprocessed.jpg"):
        print("🧪 Running Tesseract on segmented parts...")
        result = tess_extract_from_parts("parts")
        print("\n📝 Extracted + Corrected Text:\n")
        print(result)

        # Save for comparison
        with open("tesseract_output.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("✅ Saved: tesseract_output.txt")
    else:
        print("❌ preprocessed.jpg not found. Run preprocessing first.")