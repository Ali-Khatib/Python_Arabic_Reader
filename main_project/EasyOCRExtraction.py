# EasyOCRExtraction.py
import easyocr
import os

# Initialize OCR reader
reader = easyocr.Reader(['ar'], gpu=False)

def extract_arabic_text_with_lines(image_path):
    """
    Extracts Arabic text from a single image with correct reading order:
    - Top to bottom
    - Right to left per line
    """
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return ""

    results = reader.readtext(image_path, detail=1, paragraph=False)
    if not results:
        return ""

    # Sort by y (top to bottom)
    results.sort(key=lambda r: r[0][0][1])

    # Group into lines
    lines = []
    current_line = []
    last_y = None
    threshold = 30  # Line height tolerance

    for (bbox, text, prob) in results:
        y = bbox[0][1]  # Top-left y
        if last_y is None or abs(y - last_y) < threshold:
            current_line.append((bbox, text))
        else:
            # Sort right-to-left (Arabic)
            current_line.sort(key=lambda b: -b[0][0][0])
            line_text = " ".join([t for _, t in current_line])
            lines.append(line_text)
            current_line = [(bbox, text)]
        last_y = y

    # Add last line
    if current_line:
        current_line.sort(key=lambda b: -b[0][0][0])
        line_text = " ".join([t for _, t in current_line])
        lines.append(line_text)

    return "\n".join(lines)


def extract_from_parts(parts_dir="parts"):
    """
    Extracts text from all segmented parts (part_1.jpg to part_6.jpg)
    and combines them into one ordered text.
    """
    all_text = []
    for i in range(1, 7):
        part_path = os.path.join(parts_dir, f"part_{i}.jpg")
        if not os.path.exists(part_path):
            print(f"⚠️  Missing: {part_path}")
            continue  # Skip if part doesn't exist
        print(f"📄 Extracting from: {part_path}")
        text = extract_arabic_text_with_lines(part_path)
        all_text.append(text)
    return "\n".join(all_text)