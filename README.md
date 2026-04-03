# Document Analysis System

An AI-powered document processing system that extracts, analyzes, and summarizes content from PDF, DOCX, and image files with OCR support.

## 🚀 Features

- **Multi-format Support**: Process PDF, DOCX, and images (PNG, JPG, JPEG)
- **AI-Powered Summarization**: Generate concise summaries using GPT
- **Entity Extraction**: Extract names, dates, organizations, and monetary amounts
- **Sentiment Analysis**: Classify document sentiment as Positive, Neutral, or Negative
- **RESTful API**: Well-documented API with API key authentication
- **Streamlit UI**: User-friendly web interface for document upload and analysis
- **Async Processing**: Celery-based background task processing
- **OCR Support**: Tesseract OCR for image text extraction

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern web framework for API development
- **Celery**: Distributed task queue for async processing
- **Redis**: Message broker and result backend
- **Python 3.10**: Core programming language

### AI/ML
- **OpenAI GPT-3.5**: Summarization, entity extraction, sentiment analysis
- **Tesseract OCR**: Text extraction from images
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction

### Frontend
- **Streamlit**: Interactive web interface
- **Plotly**: Data visualization

## 📋 Prerequisites

- Python 3.10 or higher
- Redis server
- OpenAI API key
- Docker (optional, for containerized deployment)

## 🔧 Installation

### Option 1: Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/document-analysis-system.git
cd document-analysis-system