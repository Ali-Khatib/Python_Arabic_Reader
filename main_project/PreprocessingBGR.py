import cv2
import numpy as np
from Config import IMAGE_NAME


image_path = IMAGE_NAME

def crop_image(image_path):
    img = cv2.imread(image_path)
    h, w,_ = img.shape
    mid_y = h // 2
    mid_x = w // 2
    crop_img = img[mid_y - h // 3:mid_y + h // 2, mid_x - w // 2:mid_x + w // 2]

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    best_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            best_contour = contour

    x, y, w, h = cv2.boundingRect(best_contour)
    cropped_img = crop_img[y+67:y + h, x:x + w]
    return cropped_img

body_img = crop_image(image_path)

import cv2
import numpy as np


def preprocess_for_arabic_ocr(img):
    # ---------- GRAYSCALE & PADDING ----------
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    padded_img = cv2.copyMakeBorder(gray_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=255)

    # ---------- UPSCALE ----------
    resized_img = cv2.resize(padded_img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    # ---------- THRESHOLD & DENOISE ----------
    _, binarized = cv2.threshold(resized_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blurred = cv2.bilateralFilter(binarized, 9, 75, 75)


    # ---------- SHARPENING FILTER ----------
    kernel_sharp = np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]])
    sharpened = cv2.filter2D(blurred, -1, kernel_sharp)

    # ---------- THRESHOLD ----------
    _, thresh_img = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ---------- MORPHOLOGICAL CLEANUP ----------
    kernel_small = np.ones((1, 1), np.uint8)
    cleaned_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel_small)

    # ---------- REMOVE TINY SPECKLES ----------
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(cleaned_img, connectivity=8)
    sizes = stats[1:, -1]
    min_size = 30  # adjust: small blobs to remove
    cleaned_img = np.zeros_like(cleaned_img)
    for i in range(0, num_labels - 1):
        if sizes[i] >= min_size:
            cleaned_img[labels == i + 1] = 255

    # ---------- DILATE & CLOSE ----------
    thicker_img = cv2.dilate(cleaned_img, kernel_small, iterations=1)
    final_img = cv2.morphologyEx(thicker_img, cv2.MORPH_CLOSE, kernel_small)

    # ---------- DESKEW ----------
    coords = np.column_stack(np.where(final_img < 255))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = final_img.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(final_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return deskewed


final_image = preprocess_for_arabic_ocr(body_img)
# ✅ Save the image so OCR can read it later
cv2.imwrite("preprocessed.jpg", final_image)
print("✅ Saved: preprocessed.jpg")


# Show image with OpenCV (needs GUI support)
cv2.namedWindow("Preprocessed Image", cv2.WINDOW_NORMAL)  # create window first
cv2.resizeWindow("Preprocessed Image", 800, 1000)
cv2.imshow("Preprocessed Image", final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



