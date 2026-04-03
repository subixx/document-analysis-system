📄 DocuMind AI – Intelligent Document Analysis System

An AI-powered system to extract, analyze, and summarize content from PDFs, DOCX files, and images.

🚀 Live Demo
Service	URL
🌐 Frontend	https://documind-ai-frontend.onrender.com

⚙️ Backend API	https://documind-backend-v97h.onrender.com

📘 API Docs	https://documind-backend-v97h.onrender.com/docs
📌 Overview

DocuMind AI is a production-ready document intelligence system that uses advanced LLMs to:

Summarize documents
Extract entities (people, orgs, dates, money)
Detect sentiment
Classify document types
Identify key topics

Supports PDF, DOCX, and images (OCR-based).

✨ Key Features
📄 Multi-format support (PDF, DOCX, Images)
🧠 AI-powered summarization (context-aware)
🔍 Entity extraction (people, orgs, dates, financials)
😊 Sentiment analysis (document-aware)
🗂️ Document classification
🧩 Topic extraction
🔌 REST API support
💻 Streamlit-based UI
🛠️ Tech Stack
Backend
FastAPI – API framework
Groq LLaMA 3.3 (70B) – Core LLM
Tesseract OCR – Image text extraction
PyPDF2, python-docx – Document parsing
Docker – Deployment
Frontend
Streamlit – UI
Requests – API communication
🧠 System Architecture
1️⃣ Text Extraction Layer
Format	Method	Fallback
PDF	PyPDF2	OCR (if scanned)
DOCX	python-docx	—
Images	Tesseract OCR	—
2️⃣ AI Analysis Layer

All analysis is done using LLM (no hardcoded rules).

🔹 Summarization
Zero-shot AI summarization
Generates 2–3 line meaningful summary
🔹 Entity Extraction

Extracts:

People
Organizations
Dates
Financial values
🔹 Sentiment Analysis
Document Type	Sentiment
Resume	Neutral
Report	Positive
Incident Report	Negative
Invoice	Neutral
Research Paper	Positive
🔹 Document Classification

Detects:

Resume / CV
Report
Incident Report
Invoice
Research Paper
Email / Letter
Legal Document
💡 Why This Approach?
❌ No hardcoded rules
🧠 Fully context-aware
📊 Adapts to any document type
🚀 Production-ready design
🤖 AI Tools Used
Groq LLaMA 3.3 – Main model
OpenAI GPT (backup)
Google Gemini (optional fallback)
Tesseract OCR – Image processing
GitHub Copilot – Development support
ChatGPT / Claude – Debugging & design
⚙️ Setup Instructions
🔧 Prerequisites
Python 3.11+
Tesseract OCR installed
Groq API Key
📥 Installation
git clone https://github.com/subixx/document-analysis-system.git
cd document-analysis-system
🧪 Virtual Environment
python -m venv venv

Activate:

Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate
📦 Install Dependencies
pip install -r requirements.txt
🔑 Environment Setup
cp .env.example .env

Edit .env:

GROQ_API_KEY=your_key
API_SECRET_KEY=sk_track2_987654321
OCR_PROVIDER=tesseract
DEFAULT_LLM_MODEL=llama-3.3-70b-versatile
DEBUG=true
▶️ Run Application

Backend:

uvicorn src.api:app --reload --port 8000

Frontend:

streamlit run frontend/render_app.py
🐳 Docker (Production)
docker build -t documind-api .
docker run -p 8000:10000 -e GROQ_API_KEY=your_key documind-api
🔌 API Usage
Endpoint
POST /api/document-analyze
Headers
x-api-key: sk_track2_987654321
Request
{
  "fileName": "document.pdf",
  "fileType": "pdf",
  "fileBase64": "base64_string"
}
Response
{
  "status": "success",
  "summary": "...",
  "entities": {...},
  "sentiment": "Positive",
  "document_type": "Report",
  "key_topics": [...],
  "confidence": "high"
}
🧪 Testing
Swagger UI

👉 https://documind-backend-v97h.onrender.com/docs

Health Check
curl https://documind-backend-v97h.onrender.com/api/health
⚠️ Limitations
Issue	Details
Free Hosting	Render sleeps after inactivity
Rate Limits	Groq: 30 req/min
File Size	Max 10MB
OCR	Depends on image quality
Language	Best for English
🔐 Security
API key authentication
Input validation
Environment variable protection
CORS enabled
📁 Project Structure
document-analysis-system/
│
├── src/
│   ├── api.py
│   ├── analyzer.py
│   ├── document_processor.py
│   ├── text_extractor.py
│   └── ...
│
├── frontend/
│   └── render_app.py
│
├── requirements.txt
├── Dockerfile
├── render.yaml
└── README.md
🤝 Contributing
Fork repo
Create branch
Commit changes
Open PR
📜 License

MIT License

🙌 Acknowledgments
Groq – LLM inference
Tesseract – OCR
FastAPI – Backend framework
Streamlit – UI
Render – Hosting
👤 Author

GitHub: subixx
Project: document-analysis-system
