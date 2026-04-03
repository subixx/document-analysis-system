import pytesseract
from PIL import Image
import sys
import os

# Set Tesseract path
if sys.platform == "win32":
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        print(f"✅ Using Tesseract: {tesseract_path}")

# Check your image
image_path = "sample3.jpg"

if os.path.exists(image_path):
    print(f"\n📷 Analyzing: {image_path}")
    
    # Open image
    image = Image.open(image_path)
    print(f"Image size: {image.size}")
    print(f"Image mode: {image.mode}")
    
    # Try different OCR configurations
    print("\n🔍 Trying different OCR settings...")
    
    configs = [
        ('Default', ''),
        ('PSM 6 (Block of text)', '--psm 6'),
        ('PSM 3 (Auto)', '--psm 3'),
        ('PSM 8 (Single word)', '--psm 8'),
        ('PSM 13 (Raw line)', '--psm 13'),
    ]
    
    for name, config in configs:
        try:
            text = pytesseract.image_to_string(image, config=config)
            text_len = len(text.strip())
            print(f"  {name}: {text_len} characters extracted")
            if text_len > 10:
                print(f"    Preview: {text[:100]}")
        except Exception as e:
            print(f"  {name}: Error - {e}")
    
    # Try preprocessing
    print("\n🖼️ Trying with image preprocessing...")
    
    # Convert to grayscale
    gray = image.convert('L')
    text1 = pytesseract.image_to_string(gray)
    print(f"  Grayscale: {len(text1.strip())} chars")
    
    # Increase contrast
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(gray)
    high_contrast = enhancer.enhance(2.0)
    text2 = pytesseract.image_to_string(high_contrast)
    print(f"  High contrast: {len(text2.strip())} chars")
    
    # Resize (make larger)
    width, height = image.size
    if width < 1000 or height < 1000:
        scale = 2
        new_size = (width * scale, height * scale)
        enlarged = image.resize(new_size, Image.Resampling.LANCZOS)
        text3 = pytesseract.image_to_string(enlarged)
        print(f"  Enlarged (2x): {len(text3.strip())} chars")
    
else:
    print(f"❌ Image not found: {image_path}")