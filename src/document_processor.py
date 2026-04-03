import base64
import logging
from src.text_extractor import TextExtractor
from src.analyzer import DocumentAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self, model_name: str = None):
        self.extractor = TextExtractor()
        # Pass the model_name to analyzer
        self.analyzer = DocumentAnalyzer(model_name=model_name)
        logger.info(f"DocumentProcessor initialized with model: {model_name or 'default'}")
    
    def process_document(self, file_name: str, file_type: str, file_base64: str) -> dict:
        try:
            logger.info(f"Processing {file_name} ({file_type})")
            
            # Decode base64
            if ',' in file_base64:
                file_base64 = file_base64.split(',')[1]
            file_bytes = base64.b64decode(file_base64)
            
            # Extract text
            extracted_text = self.extractor.extract_text(file_bytes, file_type)
            
            if not extracted_text or len(extracted_text.strip()) < 10:
                return {
                    "status": "error",
                    "fileName": file_name,
                    "message": "No text could be extracted"
                }
            
            # Analyze with Groq
            analysis = self.analyzer.analyze(extracted_text)
            
            return {
                "status": "success",
                "fileName": file_name,
                "summary": analysis.get("summary", ""),
                "entities": analysis.get("entities", {
                    "people": [], "dates": [], "organizations": [], "financial": [], "other": []
                }),
                "sentiment": analysis.get("sentiment", "Neutral"),
                "document_type": analysis.get("document_type", "Unknown"),
                "key_topics": analysis.get("key_topics", []),
                "confidence": analysis.get("confidence", "medium"),
                "analyzed_by": analysis.get("analyzed_by", "System")
            }
            
        except Exception as e:
            logger.error(f"Process error: {str(e)}")
            return {
                "status": "error",
                "fileName": file_name,
                "message": str(e)
            }