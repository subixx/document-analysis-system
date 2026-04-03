from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
import logging
import traceback
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.document_processor import DocumentProcessor
from src.config import config
from src.utils import validate_file_type

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Document Analysis API",
    description="AI-Powered Document Analysis & Extraction System",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class DocumentRequest(BaseModel):
    fileName: str = Field(..., description="Name of the uploaded file")
    fileType: str = Field(..., description="Type of file: pdf, docx, or image")
    fileBase64: str = Field(..., description="Base64 encoded file content")
    model: Optional[str] = Field(None, description="LLM model to use (optional)")

class DocumentResponse(BaseModel):
    status: str
    fileName: str
    summary: str
    entities: Dict[str, Any]
    sentiment: str
    document_type: Optional[str] = None
    key_topics: Optional[List[str]] = None
    confidence: Optional[str] = None
    analyzed_by: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str
    fileName: str
    message: str

# Authentication middleware
async def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required. Please provide x-api-key header."
        )
    
    if api_key != config.API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return True

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "fileName": "unknown",
            "message": f"Internal server error: {str(exc)}"
        }
    )

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Document Analysis API",
        "version": "2.0.0",
        "debug": config.DEBUG
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "Document Analysis API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "POST /api/document-analyze",
            "health": "GET /api/health",
            "docs": "GET /docs"
        }
    }

# Main analysis endpoint
@app.post("/api/document-analyze", response_model=DocumentResponse)
async def analyze_document(request: Request, doc_request: DocumentRequest):
    logger.info(f"=== Processing request ===")
    logger.info(f"File name: {doc_request.fileName}")
    logger.info(f"File type: {doc_request.fileType}")
    logger.info(f"Requested model: {doc_request.model}")
    
    try:
        # Verify API key
        await verify_api_key(request)
        
        # Validate file type
        if not validate_file_type(doc_request.fileType):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Supported: pdf, docx, image. Got: {doc_request.fileType}"
            )
        
        # Create processor with specified model
        processor = DocumentProcessor(model_name=doc_request.model)
        result = processor.process_document(
            doc_request.fileName,
            doc_request.fileType,
            doc_request.fileBase64
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return DocumentResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# Test Gemini endpoint
@app.get("/api/test-gemini")
async def test_gemini():
    """Test Gemini connection"""
    from src.llm_provider import LLMFactory
    
    provider = LLMFactory.get_provider()
    
    if provider.available:
        return {
            "status": "success",
            "message": "Gemini is working",
            "model": provider.get_model_name()
        }
    else:
        return {
            "status": "error",
            "message": "Gemini not available",
            "api_key_configured": bool(config.GOOGLE_API_KEY)
        }

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )