import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management"""
    
    # Google Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Selection - Use the model from .env
    DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gemini-2.5-flash")
    
    # OCR Provider
    OCR_PROVIDER = os.getenv("OCR_PROVIDER", "tesseract")
    
    # API Security
    API_SECRET_KEY = os.getenv("API_SECRET_KEY", "sk_track2_987654321")
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    @classmethod
    def validate(cls):
        print("\n" + "="*50)
        print("🔧 Document Analysis System - Configuration")
        print("="*50)
        
        if cls.GOOGLE_API_KEY:
            print(f"✅ Google Gemini API Key configured")
            print(f"🎯 Using model: {cls.DEFAULT_LLM_MODEL}")
        else:
            print("❌ GOOGLE_API_KEY not set")
        
        return bool(cls.GOOGLE_API_KEY)

config = Config()