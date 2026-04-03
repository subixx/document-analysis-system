import base64
import sys
import os
import json
import traceback

# Set Tesseract path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def test_image_processing(image_path):
    """Test image processing step by step"""
    
    print("=" * 60)
    print("DIRECT IMAGE PROCESSING TEST")
    print("=" * 60)
    
    # Step 1: Check if file exists
    print(f"\n1. Checking file: {image_path}")
    if not os.path.exists(image_path):
        print(f"   ❌ File not found: {image_path}")
        return False
    print(f"   ✅ File exists")
    
    # Step 2: Read file
    print("\n2. Reading file...")
    try:
        with open(image_path, 'rb') as f:
            file_bytes = f.read()
        print(f"   ✅ Read {len(file_bytes)} bytes")
    except Exception as e:
        print(f"   ❌ Failed to read: {e}")
        return False
    
    # Step 3: Convert to base64 and back
    print("\n3. Testing base64 encoding/decoding...")
    try:
        file_base64 = base64.b64encode(file_bytes).decode()
        decoded = base64.b64decode(file_base64)
        print(f"   ✅ Base64 encoding works ({len(file_base64)} chars)")
        print(f"   ✅ Decoded back to {len(decoded)} bytes")
    except Exception as e:
        print(f"   ❌ Base64 failed: {e}")
        return False
    
    # Step 4: Test OCR directly
    print("\n4. Testing OCR directly...")
    try:
        from PIL import Image
        image = Image.open(image_path)
        print(f"   ✅ Image opened: {image.size} pixels, {image.mode}")
        
        # Try OCR
        text = pytesseract.image_to_string(image)
        print(f"   ✅ OCR completed")
        print(f"   📝 Extracted {len(text)} characters")
        if text.strip():
            print(f"\n   Preview: {text[:200]}")
        else:
            print("   ⚠️  No text extracted from image")
    except Exception as e:
        print(f"   ❌ OCR failed: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False
    
    # Step 5: Test full text extraction
    print("\n5. Testing full text extraction pipeline...")
    try:
        from src.text_extractor import TextExtractor
        extractor = TextExtractor()
        text = extractor.extract_from_image(image_path)
        print(f"   ✅ Text extraction successful")
        print(f"   📝 Extracted {len(text)} characters")
    except Exception as e:
        print(f"   ❌ Text extraction failed: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Image processing should work.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    # Test with your image
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "sample3.jpg"
    
    test_image_processing(image_path)