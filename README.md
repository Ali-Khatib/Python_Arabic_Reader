# 📄 PyArabicReader: Arabic Text Extraction from Images

> A Python-based system for extracting Arabic text from scanned or photographed documents using **EasyOCR**, with intelligent sorting for RTL languages.

This project automates the process of reading Arabic text from images by combining:
- Image preprocessing
- Segmentation into manageable parts
- Advanced OCR with correct line ordering
- Output formatting for readability

Perfect for digitizing Arabic books, documents, or handwritten notes.

---

## 🧩 Features

- ✅ Extracts Arabic text from JPG/PNG images
- ✅ Handles **right-to-left (RTL)** reading order correctly
- ✅ Supports multi-line text detection
- ✅ Preprocesses images for better OCR accuracy
- ✅ Splits large images into 6 parts for improved extraction
- ✅ Combines segmented results into coherent, ordered text
- ✅ Outputs clean, readable text to `extracted_text.txt`

---

## 🛠️ Technologies Used

- **EasyOCR**: For multilingual OCR (supports Arabic)
- **OpenCV (`cv2`)**: For image processing and segmentation
- **os.path**: For file handling
- **Python 3.10+**

---

## 📁 Project Structure
PyArabicReader/
├── main_project/
│ ├── Config.py # Image path configuration
│ ├── EasyOCRExtraction.py # Core OCR logic with RTL sorting
│ ├── main.py # Main execution flow
│ ├── PreprocessingBGR.py # Image cleanup and enhancement
│ ├── Segmentation.py # Splits image into parts
│ ├── TesseractExtraction.py # Alternative OCR backend
│ └── TransformersPostProcessing.py
│
├── pics/ # Input images (e.g., backgroundpage1.jpg)
└── extracted_text.txt # Output file


## 🚀 How It Works

1. **Preprocessing**: Enhances image quality for better OCR.
2. **Segmentation**: Divides the page into 6 parts to avoid skew and noise.
3. **OCR**: Runs EasyOCR on each segment, detecting Arabic text.
4. **Sorting**: Groups detected words into lines (top-to-bottom, right-to-left).
5. **Output**: Saves full text to `extracted_text.txt`.

---

## 🧪 Example Usage

1. Place your input image in `pics/` (e.g., `backgroundpage1.jpg`)
2. Run the script:

```bash
python main.py
