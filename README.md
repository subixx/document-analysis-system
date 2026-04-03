# 📄 DocuMind AI - Intelligent Document Analysis System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41-red.svg)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3-orange.svg)](https://groq.com)

An intelligent document processing system that extracts, analyzes, and summarizes content from various document formats (PDF, DOCX, images) using AI-powered technology.

## 🚀 Live Demo

| Service | URL |
|---------|-----|
| **Frontend UI** | [https://documind-ai-frontend.onrender.com](https://documind-ai-frontend.onrender.com) |
| **Backend API** | [https://documind-backend-v97h.onrender.com](https://documind-backend-v97h.onrender.com) |
| **API Documentation** | [https://documind-backend-v97h.onrender.com/docs](https://documind-backend-v97h.onrender.com/docs) |

## 📋 Description

DocuMind AI is a production-ready document analysis system that leverages Groq's Llama 3.3 70B model to intelligently extract and analyze information from documents. The system supports multiple formats (PDF, DOCX, images) and provides AI-powered summarization, entity extraction, sentiment analysis, and document classification.

### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-format Support** | Process PDF, DOCX, and images (with OCR fallback) |
| **AI-Powered Summarization** | Generate concise, meaningful summaries using Groq Llama 3.3 |
| **Entity Extraction** | Automatically identify people, organizations, dates, and financial amounts |
| **Sentiment Analysis** | Classify document sentiment based on content and document type |
| **Document Classification** | Identify document types (Resume/CV, Report, Incident Report, etc.) |
| **Topic Extraction** | Extract key topics and themes from documents |
| **RESTful API** | Simple, authenticated API for programmatic access |
| **Web Interface** | User-friendly Streamlit UI for easy testing |

## 🛠️ Tech Stack

### Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | REST API development |
| LLM | Groq Llama 3.3 70B | AI-powered analysis |
| OCR | Tesseract | Text extraction from images |
| Document Parsing | PyPDF2, python-docx | PDF/DOCX extraction |
| Container | Docker | Deployment with dependencies |

### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| UI Framework | Streamlit | Web interface |
| HTTP Client | Requests | API communication |

### Key Libraries
fastapi==0.115.6
uvicorn==0.34.0
streamlit==1.41.1
PyPDF2==3.0.1
python-docx==1.1.2
pytesseract==0.3.13
Pillow==11.1.0
groq==0.13.0
pdf2image==1.17.0

## 🧠 Approach & Strategy

### Data Extraction Strategy

Our approach focuses on **pure AI-driven analysis** without hardcoded rules or patterns.

#### 1. Text Extraction Layer

| Document Type | Method | Fallback |
|---------------|--------|----------|
| **PDF** | Direct text extraction with PyPDF2 | OCR for scanned documents |
| **DOCX** | Structure-preserving extraction using python-docx | - |
| **Images** | Tesseract OCR with preprocessing (grayscale, contrast enhancement) | - |

#### 2. AI-Powered Analysis Layer

The system uses Groq's Llama 3.3 70B model for all analysis tasks:

**Summarization:**
- **Approach**: Zero-shot summarization using LLM
- **Process**: AI reads entire document and generates concise 2-3 sentence summary
- **Key Feature**: No template-based summaries - AI understands context and extracts main ideas

**Entity Extraction:**
- **Approach**: Context-aware entity recognition using LLM
- **Entity Types**:
  - **People**: Extracts actual person names (not job titles or skills)
  - **Organizations**: Companies, institutions, universities
  - **Dates**: Years, specific dates, date ranges
  - **Financial**: Monetary amounts with currency symbols
- **Key Feature**: AI distinguishes between names, job titles, and skills based on context

**Sentiment Analysis:**

| Document Type | Sentiment | Reason |
|---------------|-----------|--------|
| Resume/CV | Neutral | Professional self-presentation |
| Report / Industry Analysis | Positive | Growth, innovation focus |
| Incident Report | Negative | Describes problems/breaches |
| Invoice | Neutral | Purely transactional |
| Research Paper | Positive | Highlights improvements/discoveries |
| Email/Letter | Context-driven | Preserves AI analysis |
| Legal Document | Neutral | Formal, no emotional tone |

**Document Classification:**
- **Approach**: AI identifies document type based on content patterns
- **Types Detected**: Resume/CV, Invoice, Report, Incident Report, Research Paper, Email/Letter, Legal Document

### Why This Approach Works

| Advantage | Description |
|-----------|-------------|
| **No Hardcoded Rules** | System adapts to any document type without predefined patterns |
| **Context-Aware** | AI understands the difference between a name and a job title |
| **Document-Type Specific** | Sentiment and entity extraction vary based on document context |
| **Production-Ready** | Authentication, error handling, and logging included |

## 🤖 AI Tools Used

| Tool | Purpose | Usage |
|------|---------|-------|
| **Groq Llama 3.3 70B** | Main LLM for document analysis | Summarization, entity extraction, sentiment analysis |
| **OpenAI GPT-3.5** | Backup LLM (if Groq unavailable) | Fallback analysis |
| **Google Gemini** | Alternative LLM | Optional backup |
| **Tesseract OCR** | Optical Character Recognition | Text extraction from images |
| **GitHub Copilot** | Code assistance | Helped with boilerplate code, debugging |
| **ChatGPT (OpenAI)** | Code review and debugging | Helped resolve API integration issues, dependency conflicts |
| **Claude (Anthropic)** | Architecture design | Assisted with prompt engineering and system design |

## 📦 Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Tesseract OCR installed on your system
- Groq API key (free from [console.groq.com](https://console.groq.com))

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/subixx/document-analysis-system.git
cd document-analysis-system
#### **2. Create Virtual Environment**
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
#### **3. Install Dependencies**
bash
pip install -r requirements.txt
#### **4. Install Tesseract OCR**
Windows:

powershell
# Download from: https://github.com/UB-Mannheim/tesseract/releases
# Install with "Add to PATH" option
macOS:

bash
brew install tesseract
Linux:

bash
sudo apt-get install tesseract-ocr
#### **5. Configure Environment Variables**
bash
cp .env.example .env
Edit .env file:

env
GROQ_API_KEY=your_groq_api_key_here
API_SECRET_KEY=sk_track2_987654321
OCR_PROVIDER=tesseract
DEFAULT_LLM_MODEL=llama-3.3-70b-versatile
DEBUG=true
#### **6. Run the Application**
Terminal 1 - API Backend:

bash
uvicorn src.api:app --reload --port 8000
Terminal 2 - Streamlit Frontend:

bash
streamlit run frontend/render_app.py
Docker Setup (Recommended for Production)
bash
# Build Docker image
docker build -t documind-api .

# Run container
docker run -p 8000:10000 -e GROQ_API_KEY=your_key documind-api
Deploy to Render
Push code to GitHub

Create new Web Service on Render

Select "Docker" as runtime

Add environment variables:

GROQ_API_KEY

API_SECRET_KEY

OCR_PROVIDER

####**🔌 API Documentation**
Authentication
All API requests require an API key in the header:

http
x-api-key: sk_track2_987654321
Endpoint
text
POST /api/document-analyze
Request Format
json
{
    "fileName": "document.pdf",
    "fileType": "pdf",
    "fileBase64": "base64_encoded_content"
}
**Response Format**
json
{
    "status": "success",
    "fileName": "document.pdf",
    "summary": "AI-generated summary of the document...",
    "entities": {
        "people": ["John Doe", "Jane Smith"],
        "dates": ["2024", "March 15, 2024"],
        "organizations": ["Google", "Microsoft"],
        "financial": ["$50,000", "₹10,000"],
        "other": []
    },
    "sentiment": "Positive",
    "document_type": "Report",
    "key_topics": ["Artificial Intelligence", "Innovation", "Growth"],
    "confidence": "high",
    "analyzed_by": "Groq/llama-3.3-70b-versatile"
}
**cURL Example**
bash
curl -X POST https://documind-backend-v97h.onrender.com/api/document-analyze \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_track2_987654321" \
  -d '{
    "fileName": "sample.pdf",
    "fileType": "pdf",
    "fileBase64": "base64_encoded_content"
  }'
Python Example
python
import requests
import base64

url = "https://documind-backend-v97h.onrender.com/api/document-analyze"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "sk_track2_987654321"
}

with open("document.pdf", "rb") as f:
    file_base64 = base64.b64encode(f.read()).decode()

payload = {
    "fileName": "document.pdf",
    "fileType": "pdf",
    "fileBase64": file_base64
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
#### **Project Structure**
text
document-analysis-system/
├── src/
│   ├── __init__.py
│   ├── api.py              # FastAPI endpoints
│   ├── analyzer.py         # AI analysis logic
│   ├── config.py           # Configuration management
│   ├── document_processor.py # Document processing orchestration
│   ├── text_extractor.py   # OCR and text extraction
│   ├── llm_provider.py     # Groq API integration
│   ├── ocr_provider.py     # OCR provider (Tesseract/Google Vision)
│   └── utils.py            # Utility functions
├── frontend/
│   └── render_app.py       # Streamlit UI
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── render.yaml            # Render deployment config
├── .env.example           # Environment variables template
└── README.md              # This file
**📊 API Testing**
Test with Swagger UI
Open in browser: https://documind-backend-v97h.onrender.com/docs

**Test with Health Check**
bash
curl https://documind-backend-v97h.onrender.com/api/health
Expected response:

json
{"status":"healthy","service":"Document Analysis API","version":"2.0.0","debug":true}
** Known Limitations
Limitation	Description**
Free Tier Limits	Render services spin down after 15 minutes (30-60s wake time)
Rate Limiting	Groq API: 30 requests per minute
File Size	Maximum 10MB file size
OCR Accuracy	Depends on image quality and text clarity
Language Support	Primarily optimized for English text
** Security**
API key authentication required for all endpoints
CORS configured for cross-origin requests
Environment variables for sensitive data
Input validation and sanitization

**Contributing**
Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Open a Pull Request

#### **License**
MIT License - See LICENSE file for details

#### **Acknowledgments**
Groq for providing fast, free LLM inference
Tesseract OCR for OCR capabilities
FastAPI for the excellent web framework
Streamlit for the beautiful UI framework
Render for free hosting

**Contact**
GitHub: subixx
Project Link: document-analysis-system


