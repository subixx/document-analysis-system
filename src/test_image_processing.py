import sys
import os
import cv2
import pytesseract
from PIL import Image

# Set Tesseract path for Windows
if sys.platform == "win32":
    tesseract_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    for path in tesseract_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            print(f"Using Tesseract: {path}")
            break

def test_image_ocr(image_path):
    """Test OCR on an image"""
    print(f"\nTesting image: {image_path}")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
    
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            print("❌ Could not read image with OpenCV")
            # Try with PIL
            image = Image.open(image_path)
            print("✓ Read image with PIL")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Extract text
        text = pytesseract.image_to_string(thresh, lang='eng')
        
        print(f"✓ Extracted {len(text)} characters")
        print("\n--- Extracted Text ---")
        print(text[:500])  # Print first 500 chars
        print("--- End of Text ---\n")
        
        return text
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Test with your image
    test_image_ocr("sample3.jpg")