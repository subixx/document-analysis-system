import streamlit as st
import requests
import base64
import json
from pathlib import Path
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
    }
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .topic-tag {
        background: #e0e7ff;
        color: #4338ca;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Retry function for rate limits
def make_request_with_retry(url, payload, headers, max_retries=3):
    """Make API request with automatic retry on rate limits"""
    for attempt in range(max_retries):
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        
        if response.status_code == 429:
            wait_time = (attempt + 1) * 5  # 5, 10, 15 seconds
            st.warning(f"Rate limit hit. Waiting {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
            continue
        
        return response
    
    return response

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0;">DocuMind AI</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">Intelligent Document Analysis & Extraction</p>
    <p style="margin: 0; font-size: 0.75rem; opacity: 0.7;">Powered by Groq Llama 3.3</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Configuration")
    
    api_url = st.text_input(
        "API URL",
        value="https://document-analysis-system.onrender.com/api/document-analyze",
        help="Your deployed API URL"
    )
    
    api_key = st.text_input(
        "API Key",
        value="sk_track2_987654321",
        type="password"
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("Upload PDF, DOCX, or images for AI-powered analysis.")

# Main content
st.markdown("### Upload Document")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=['pdf', 'docx', 'png', 'jpg', 'jpeg'],
    label_visibility="collapsed"
)

if uploaded_file:
    file_name = uploaded_file.name
    file_content = uploaded_file.read()
    
    ext = Path(file_name).suffix.lower()
    if ext == '.pdf':
        file_type = 'pdf'
    elif ext == '.docx':
        file_type = 'docx'
    else:
        file_type = 'image'
    
    st.markdown(f"""
    <div class="info-box">
        <strong>File loaded:</strong> {file_name}<br>
        <strong>Size:</strong> {len(file_content) / 1024:.2f} KB<br>
        <strong>Type:</strong> {file_type.upper()}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Analyze Document", use_container_width=True):
        with st.spinner("Analyzing document..."):
            try:
                file_base64 = base64.b64encode(file_content).decode('utf-8')
                
                payload = {
                    "fileName": file_name,
                    "fileType": file_type,
                    "fileBase64": file_base64
                }
                
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": api_key
                }
                
                # Use retry function
                response = make_request_with_retry(api_url, payload, headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("### Results")
                    
                    # Summary
                    st.markdown(f'<div class="success-box">{result["summary"]}</div>', unsafe_allow_html=True)
                    
                    # Document info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Document Type", result.get("document_type", "Unknown"))
                    with col2:
                        st.metric("Sentiment", result.get("sentiment", "Neutral"))
                    with col3:
                        st.metric("Confidence", result.get("confidence", "N/A").upper())
                    
                    # Key topics
                    if result.get("key_topics"):
                        st.markdown("**Key Topics:**")
                        topics_html = "".join([f'<span class="topic-tag">{topic}</span>' for topic in result["key_topics"]])
                        st.markdown(f'<div>{topics_html}</div>', unsafe_allow_html=True)
                    
                    # Entities
                    entities = result.get("entities", {})
                    if any(entities.values()):
                        st.markdown("### Extracted Entities")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if entities.get("people"):
                                st.markdown("**People**")
                                for p in entities["people"]:
                                    st.markdown(f"- {p}")
                            if entities.get("organizations"):
                                st.markdown("**Organizations**")
                                for o in entities["organizations"]:
                                    st.markdown(f"- {o}")
                        with col_b:
                            if entities.get("dates"):
                                st.markdown("**Dates**")
                                for d in entities["dates"]:
                                    st.markdown(f"- {d}")
                            if entities.get("financial"):
                                st.markdown("**Financial**")
                                for f in entities["financial"]:
                                    st.markdown(f"- {f}")
                    
                    # Model info
                    st.caption(f"Analyzed by: {result.get('analyzed_by', 'Unknown')}")
                    
                    # Download
                    st.download_button(
                        label="Download Results (JSON)",
                        data=json.dumps(result, indent=2),
                        file_name=f"{Path(file_name).stem}_analysis.json",
                        mime="application/json"
                    )
                    
                elif response.status_code == 429:
                    st.error("Rate limit exceeded. Please wait a moment and try again.")
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.code(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot connect to API at {api_url}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
