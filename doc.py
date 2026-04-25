import sys
import streamlit as st

st.write("Python version:", sys.version)

try:
    import cv2
    st.success("cv2 imported successfully")
except Exception as e:
    st.error(f"cv2 error: {e}")
    st.stop()import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
st.set_page_config(page_title="Document Scanner", layout="wide")

st.title("📄 Smart Document Scanner + OCR")

uploaded_file = st.file_uploader("Upload Document Image", type=["jpg", "png", "jpeg"])


def scan_document(image):
    # Convert to grayscale safely
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur + Edge detection
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 75, 200)

    return gray, edged


if uploaded_file:
    # ✅ Force image to RGB (prevents channel issues)
    image = Image.open(uploaded_file).convert("RGB")

    # Convert to numpy array
    image = np.array(image)

    # Convert RGB → BGR (OpenCV format)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    st.subheader("Original Image")
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_column_width=True)

    # Scan document
    gray, scanned = scan_document(image)

    st.subheader("Grayscale")
    st.image(gray, use_column_width=True, channels="GRAY")

    st.subheader("Edge Detection (Scanner View)")
    st.image(scanned, use_column_width=True)

    # ✅ Improve OCR accuracy
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh)

    st.subheader("Extracted Text")
    st.text_area("OCR Output", text, height=200)

    # Save text
    file_path = "scanned_text.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    st.success("Text saved as scanned_text.txt")

    # Download button
    st.download_button(
        label="Download Text File",
        data=text,
        file_name="scanned_text.txt",
        mime="text/plain"
    )

    
