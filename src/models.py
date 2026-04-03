from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from enum import Enum

class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class DocumentRequest(BaseModel):
    """Request model for document analysis"""
    fileName: str = Field(..., description="Name of the uploaded file", min_length=1, max_length=255)
    fileType: FileType = Field(..., description="Type of the document")
    fileBase64: str = Field(..., description="Base64 encoded file content")
    
    @validator('fileBase64')
    def validate_base64(cls, v):
        import base64
        try:
            base64.b64decode(v)
            return v
        except:
            raise ValueError('Invalid base64 encoding')

class Entities(BaseModel):
    """Extracted entities model"""
    names: List[str] = Field(default_factory=list, description="Person names found")
    dates: List[str] = Field(default_factory=list, description="Dates found")
    organizations: List[str] = Field(default_factory=list, description="Organizations found")
    amounts: List[str] = Field(default_factory=list, description="Monetary amounts found")

class DocumentResponse(BaseModel):
    """Response model for document analysis"""
    status: str = Field(..., description="Success or error status")
    fileName: str = Field(..., description="Original file name")
    summary: str = Field(..., description="AI-generated summary (max 3 lines)")
    entities: Entities = Field(..., description="Extracted entities")
    sentiment: Sentiment = Field(..., description="Document sentiment")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "fileName": "invoice.pdf",
                "summary": "Invoice from ABC Pvt Ltd to Ravi Kumar dated 10 March 2026 for ₹10,000.",
                "entities": {
                    "names": ["Ravi Kumar"],
                    "dates": ["10 March 2026"],
                    "organizations": ["ABC Pvt Ltd"],
                    "amounts": ["₹10,000"]
                },
                "sentiment": "neutral"
            }
        }