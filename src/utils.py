import base64
import io
import tempfile
import os
from typing import Tuple, Optional
from PIL import Image

def decode_base64_file(base64_string: str) -> bytes:
    """Decode base64 string to bytes"""
    # Remove data URL prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    return base64.b64decode(base64_string)

def save_temp_file(file_content: bytes, file_extension: str) -> str:
    """Save file content to temporary file and return path"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(file_content)
        return tmp_file.name

def cleanup_temp_file(file_path: str):
    """Remove temporary file"""
    if os.path.exists(file_path):
        os.unlink(file_path)

def validate_file_type(file_type: str) -> bool:
    """Validate file type"""
    allowed = {"pdf", "docx", "image"}
    return file_type.lower() in allowed