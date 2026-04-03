FROM python:3.11-slim

# Install Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV OCR_PROVIDER=tesseract
ENV DEFAULT_LLM_MODEL=llama-3.3-70b-versatile

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "10000"]
