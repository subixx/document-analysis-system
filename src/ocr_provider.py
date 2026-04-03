import os
import logging
import base64
from abc import ABC, abstractmethod
from PIL import Image
import io
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCRProvider(ABC):
    """Abstract OCR provider"""
    
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> str:
        """Extract text from image"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider name"""
        pass


class TesseractOCRProvider(OCRProvider):
    """Tesseract OCR - Free, local"""
    
    def __init__(self):
        try:
            import pytesseract
            from PIL import ImageEnhance, ImageFilter
            
            self.pytesseract = pytesseract
            self.ImageEnhance = ImageEnhance
            self.ImageFilter = ImageFilter
            
            # Set Tesseract path for Windows
            import sys
            if sys.platform == "win32":
                possible_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        break
            
            # Test Tesseract
            pytesseract.get_tesseract_version()
            self.available = True
            logger.info("✅ Tesseract OCR initialized successfully")
            
        except Exception as e:
            logger.error(f"Tesseract not available: {str(e)}")
            self.available = False
    
    def extract_text(self, image_bytes: bytes) -> str:
        """Extract text using Tesseract"""
        if not self.available:
            return "Tesseract OCR is not installed. Please install it or switch to Google Cloud Vision."
        
        try:
            # Open image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Preprocess for better OCR
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = self.ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Perform OCR with multiple PSM modes
            text = self.pytesseract.image_to_string(image, config='--psm 3')
            
            if not text.strip():
                # Try different PSM mode for sparse text
                text = self.pytesseract.image_to_string(image, config='--psm 6')
            
            return text.strip() if text.strip() else "No text detected in image."
            
        except Exception as e:
            logger.error(f"Tesseract OCR error: {str(e)}")
            return f"OCR failed: {str(e)}"
    
    def get_provider_name(self) -> str:
        return "Tesseract OCR (Local)"


class GoogleVisionOCRProvider(OCRProvider):
    """Google Cloud Vision API - Cloud-based, more accurate"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_CLOUD_VISION_API_KEY")
        self.available = bool(self.api_key)
        
        if self.available:
            logger.info("✅ Google Cloud Vision API initialized")
        else:
            logger.warning("Google Cloud Vision API key not set")
    
    def extract_text(self, image_bytes: bytes) -> str:
        """Extract text using Google Cloud Vision API"""
        if not self.available:
            return "Google Cloud Vision API key not configured."
        
        try:
            import requests
            
            # Encode image to base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Prepare API request
            url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"
            
            payload = {
                "requests": [{
                    "image": {"content": image_base64},
                    "features": [{"type": "TEXT_DETECTION"}]
                }]
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if 'responses' in result and result['responses']:
                text_annotation = result['responses'][0].get('fullTextAnnotation', {})
                text = text_annotation.get('text', '')
                return text.strip() if text.strip() else "No text detected in image."
            
            return "No text detected in image."
            
        except Exception as e:
            logger.error(f"Google Vision OCR error: {str(e)}")
            return f"Google Vision OCR failed: {str(e)}"
    
    def get_provider_name(self) -> str:
        return "Google Cloud Vision API"


class OCRFactory:
    """Factory to create OCR provider"""
    
    @staticmethod
    def get_provider(provider_name: str = None) -> OCRProvider:
        """Get OCR provider based on configuration"""
        
        provider_name = provider_name or os.getenv("OCR_PROVIDER", "tesseract")
        
        if provider_name.lower() == "google_vision":
            return GoogleVisionOCRProvider()
        else:
            # Default to Tesseract
            return TesseractOCRProvider()