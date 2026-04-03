import os
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqProvider:
    def __init__(self, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.available = False
        self.client = None
        
        logger.info(f"Initializing Groq with model: {self.model}")
        
        if not self.api_key:
            logger.error("❌ GROQ_API_KEY not found")
            return
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            
            # Quick test
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "OK"}],
                max_tokens=5
            )
            
            if test_response:
                self.available = True
                logger.info(f"✅ Groq ready with model: {self.model}")
                
        except ImportError:
            logger.error("❌ Groq package not installed. Run: pip install groq")
        except Exception as e:
            logger.error(f"❌ Groq error: {e}")
    
    def analyze(self, prompt: str, text: str) -> str:
        if not self.available:
            return ""
        
        try:
            max_length = 15000
            truncated_text = text[:max_length] if len(text) > max_length else text
            
            full_prompt = f"{prompt}\n\nDOCUMENT TEXT:\n{truncated_text}\n\nReturn ONLY valid JSON. No markdown."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert document analyzer. Return ONLY valid JSON."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Groq error: {e}")
            return ""
    
    def get_model_name(self) -> str:
        return f"Groq/{self.model}"


class LLMFactory:
    @staticmethod
    def get_provider(model_name: str = None):
        return GroqProvider(model=model_name)