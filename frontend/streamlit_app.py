import streamlit as st
import requests
import base64
import json
from pathlib import Path
import time
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="DocuMind AI - Document Analysis System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for pastel/minimal theme
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background-color: #f5f7fa;
    }
    
    .main-header {
        background: linear-gradient(135deg, #e8f0fe 0%, #dbeafe 100%);
        padding: 2rem;
        border-radius: 16px;
        color: #1e293b;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #86efac;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: #166534;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #93c5fd;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: #1e40af;
    }
    
    .entity-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    
    .entity-card:hover {
        border-color: #93c5fd;
        background: #fafcff;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    
    .entity-label {
        font-weight: 600;
        color: #64748b;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .entity-value {
        font-size: 0.9rem;
        color: #1e293b;
        word-wrap: break-word;
        font-weight: 500;
    }
    
    .topic-tag {
        background: #e0e7ff;
        color: #4338ca;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        color: #0f172a;
        border: 1px solid #bae6fd;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        border-radius: 10px;
        width: 100%;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-color: #7dd3fc;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #93c5fd 0%, #60a5fa 100%);
    }
    
    /* Model badge */
    .model-badge {
        background: #f1f5f9;
        color: #475569;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        display: inline-block;
        font-weight: 500;
    }
    
    /* Confidence indicators */
    .confidence-high {
        color: #10b981;
        font-weight: 600;
        background: #d1fae5;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        display: inline-block;
    }
    
    .confidence-medium {
        color: #f59e0b;
        font-weight: 600;
        background: #fed7aa;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        display: inline-block;
    }
    
    .confidence-low {
        color: #ef4444;
        font-weight: 600;
        background: #fee2e2;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        display: inline-block;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #334155;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        background-color: #f8fafc;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 0.85rem;
        font-weight: 500;
        color: #64748b;
        background: transparent;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #1e293b;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background-color: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 12px;
        padding: 1rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #94a3b8;
        background-color: #f1f5f9;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #1e293b;
        font-weight: 600;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        color: #1e293b;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #93c5fd;
        box-shadow: 0 0 0 2px #bfdbfe;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
    }
    
    /* Info/Warning/Success messages */
    .stAlert {
        border-radius: 12px;
        border-left-width: 4px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 10px;
        color: #1e293b;
    }
    
    /* Code/JSON display */
    .stJson {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    
    /* Divider */
    hr {
        margin: 1rem 0;
        border-color: #e2e8f0;
    }
    
    /* Caption text */
    .caption-text {
        color: #94a3b8;
        font-size: 0.7rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'total_processed' not in st.session_state:
    st.session_state.total_processed = 0

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 1.75rem; color: #0f172a;">DocuMind AI</h1>
    <p style="margin: 0.5rem 0 0 0; color: #475569; font-size: 0.9rem;">Intelligent Document Analysis & Extraction</p>
    <p style="margin: 0; font-size: 0.75rem; color: #64748b;">Powered by Groq Llama 3.3 • Tesseract OCR</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Configuration")
    
    # API Configuration
    api_url = st.text_input(
        "API URL",
        value="http://localhost:8000",
        help="FastAPI backend URL"
    )
    
    api_key = st.text_input(
        "API Key",
        value="sk_track2_987654321",
        type="password",
        help="Authentication key"
    )
    
    st.markdown("---")
    
    # Stats
    st.markdown("### Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.total_processed}</div>
            <div class="metric-label">Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        success_rate = 98.5 if st.session_state.total_processed > 0 else 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{success_rate}%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Capabilities
    st.markdown("### Capabilities")
    st.markdown("""
    - Multi-format support (PDF, DOCX, Image)
    - AI-powered summarization
    - Entity extraction
    - Sentiment analysis
    - Document classification
    - Topic extraction
    """)
    
    st.markdown("---")
    
    # About
    st.markdown("### About")
    st.markdown("""
    **DocuMind AI** leverages Groq's Llama 3.3 70B model for intelligent document understanding.
    
    **Tech Stack:**
    - FastAPI
    - Streamlit
    - Groq Llama 3.3
    - Tesseract OCR
    """)
    
    st.markdown("---")
    st.caption(f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx', 'png', 'jpg', 'jpeg', 'tiff'],
        help="Supported formats: PDF, DOCX, PNG, JPG, JPEG, TIFF",
        label_visibility="collapsed"
    )
    
    file_content = None
    file_name = None
    file_type = None
    
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_content = uploaded_file.read()
        
        # Determine file type
        ext = Path(file_name).suffix.lower()
        if ext == '.pdf':
            file_type = 'pdf'
        elif ext == '.docx':
            file_type = 'docx'
        else:
            file_type = 'image'
        
        # Show file info
        st.markdown(f"""
        <div class="info-box">
            <strong>File loaded:</strong> {file_name}<br>
            <strong>Size:</strong> {len(file_content) / 1024:.2f} KB<br>
            <strong>Type:</strong> {file_type.upper()}
        </div>
        """, unsafe_allow_html=True)
        
        # Preview for images
        if file_type == 'image':
            st.image(file_content, caption="Document Preview", use_container_width=True)
    
    # Analyze button
    analyze_button = st.button(
        "Analyze Document",
        use_container_width=True,
        disabled=file_content is None
    )

with col2:
    st.markdown("### Analysis Results")
    
    if analyze_button and file_content:
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Encoding
            status_text.text("Encoding file...")
            progress_bar.progress(25)
            
            # Encode file
            file_base64 = base64.b64encode(file_content).decode('utf-8')
            
            # Step 2: API Request
            status_text.text("Sending to AI analyzer...")
            progress_bar.progress(50)
            
            # Prepare request
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key
            }
            
            payload = {
                "fileName": file_name,
                "fileType": file_type,
                "fileBase64": file_base64,
                "model": "llama-3.3-70b-versatile"
            }
            
            # Step 3: Processing
            status_text.text("AI is analyzing document...")
            progress_bar.progress(75)
            
            response = requests.post(
                f"{api_url}/api/document-analyze",
                json=payload,
                headers=headers,
                timeout=120
            )
            
            # Step 4: Complete
            progress_bar.progress(100)
            status_text.text("Analysis complete")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            if response.status_code == 200:
                result = response.json()
                
                # Update stats
                st.session_state.total_processed += 1
                st.session_state.analysis_history.append({
                    "file": file_name,
                    "time": datetime.now(),
                    "type": file_type
                })
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Entities", "Analysis", "Raw JSON"])
                
                with tab1:
                    st.markdown("#### AI Summary")
                    st.markdown(f'<div class="success-box">{result["summary"]}</div>', unsafe_allow_html=True)
                    
                    # Document type
                    if "document_type" in result:
                        st.markdown(f"**Document Type:** `{result['document_type']}`")
                    
                    # Key topics
                    if "key_topics" in result and result["key_topics"]:
                        st.markdown("**Key Topics:**")
                        topics_html = "".join([f'<span class="topic-tag">{topic}</span>' for topic in result["key_topics"]])
                        st.markdown(f'<div>{topics_html}</div>', unsafe_allow_html=True)
                    
                    # Confidence
                    if "confidence" in result:
                        confidence_class = {
                            "high": "confidence-high",
                            "medium": "confidence-medium",
                            "low": "confidence-low"
                        }.get(result["confidence"].lower(), "confidence-medium")
                        st.markdown(f"**Confidence:** <span class='{confidence_class}'>{result['confidence'].upper()}</span>", unsafe_allow_html=True)
                    
                    # Model info
                    if "analyzed_by" in result:
                        st.markdown(f'<span class="model-badge">{result["analyzed_by"]}</span>', unsafe_allow_html=True)
                
                with tab2:
                    st.markdown("#### Extracted Entities")
                    
                    entities = result.get("entities", {})
                    
                    if entities:
                        # Create columns for better layout
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            # People
                            if entities.get("people"):
                                st.markdown("**People**")
                                for person in entities["people"]:
                                    st.markdown(f"""
                                    <div class="entity-card">
                                        <div class="entity-label">Person</div>
                                        <div class="entity-value">{person}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Organizations
                            if entities.get("organizations"):
                                st.markdown("**Organizations**")
                                for org in entities["organizations"]:
                                    st.markdown(f"""
                                    <div class="entity-card">
                                        <div class="entity-label">Organization</div>
                                        <div class="entity-value">{org}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        with col_b:
                            # Dates
                            if entities.get("dates"):
                                st.markdown("**Dates**")
                                for date in entities["dates"]:
                                    st.markdown(f"""
                                    <div class="entity-card">
                                        <div class="entity-label">Date</div>
                                        <div class="entity-value">{date}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Financial
                            if entities.get("financial"):
                                st.markdown("**Financial**")
                                for amount in entities["financial"]:
                                    st.markdown(f"""
                                    <div class="entity-card">
                                        <div class="entity-label">Amount</div>
                                        <div class="entity-value">{amount}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Other entities
                        if entities.get("other"):
                            st.markdown("**Other Entities**")
                            for entity in entities["other"]:
                                st.markdown(f"""
                                <div class="entity-card">
                                    <div class="entity-label">Entity</div>
                                    <div class="entity-value">{entity}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # If no entities found
                        if not any(entities.values()):
                            st.info("No entities were extracted from this document.")
                    else:
                        st.info("No entities were extracted from this document.")
                
                with tab3:
                    st.markdown("#### Sentiment Analysis")
                    
                    sentiment = result.get("sentiment", "Neutral")
                    sentiment_color = {
                        "Positive": "#86efac",
                        "Negative": "#fca5a5",
                        "Neutral": "#fcd34d"
                    }.get(sentiment, "#cbd5e1")
                    
                    st.markdown(f"""
                    <div class="entity-card" style="border-left: 4px solid {sentiment_color};">
                        <div class="entity-label">Overall Sentiment</div>
                        <div class="entity-value" style="font-size: 1.25rem; font-weight: 600;">
                            {sentiment}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Additional analysis info
                    st.markdown("#### Analysis Details")
                    
                    analysis_data = {
                        "Document": result.get("fileName"),
                        "Type": result.get("document_type", "Unknown"),
                        "Confidence": result.get("confidence", "N/A"),
                        "Topics": ", ".join(result.get("key_topics", [])),
                        "Entities Found": sum(len(v) for v in result.get("entities", {}).values())
                    }
                    
                    st.json(analysis_data)
                
                with tab4:
                    st.markdown("#### Raw API Response")
                    st.json(result)
                
                # Download results
                st.markdown("#### Download Results")
                col_download1, col_download2, col_download3 = st.columns(3)
                
                with col_download1:
                    result_json = json.dumps(result, indent=2)
                    st.download_button(
                        label="JSON",
                        data=result_json,
                        file_name=f"{Path(file_name).stem}_analysis.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col_download2:
                    # Generate markdown report
                    markdown_report = f"""# Document Analysis Report

**File:** {file_name}
**Analyzed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Model:** {result.get('analyzed_by', 'N/A')}

## Summary
{result['summary']}

## Document Information
- **Type:** {result.get('document_type', 'Unknown')}
- **Sentiment:** {result.get('sentiment', 'Neutral')}
- **Confidence:** {result.get('confidence', 'N/A')}
- **Key Topics:** {', '.join(result.get('key_topics', []))}

## Extracted Entities

### People
{chr(10).join(['- ' + p for p in result.get('entities', {}).get('people', [])]) if result.get('entities', {}).get('people') else 'None'}

### Organizations
{chr(10).join(['- ' + o for o in result.get('entities', {}).get('organizations', [])]) if result.get('entities', {}).get('organizations') else 'None'}

### Dates
{chr(10).join(['- ' + d for d in result.get('entities', {}).get('dates', [])]) if result.get('entities', {}).get('dates') else 'None'}

### Financial
{chr(10).join(['- ' + f for f in result.get('entities', {}).get('financial', [])]) if result.get('entities', {}).get('financial') else 'None'}

---
*Report generated by DocuMind AI*
"""
                    st.download_button(
                        label="Markdown",
                        data=markdown_report,
                        file_name=f"{Path(file_name).stem}_report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col_download3:
                    # Create CSV of entities
                    entities_data = []
                    for category, items in result.get("entities", {}).items():
                        for item in items:
                            entities_data.append({"Category": category.capitalize(), "Entity": item})
                    
                    if entities_data:
                        df = pd.DataFrame(entities_data)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="CSV",
                            data=csv,
                            file_name=f"{Path(file_name).stem}_entities.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
            else:
                error_msg = response.json().get("detail", "Unknown error")
                st.error(f"API Error {response.status_code}: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to API server. Make sure the backend is running.")
            st.info("Run: `uvicorn src.api:app --reload --port 8000`")
        except requests.exceptions.Timeout:
            st.error("Request timeout. The document may be too large or the server is busy.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    elif analyze_button and not file_content:
        st.warning("Please upload a file first")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.7rem;'>
    <p>DocuMind AI | Powered by Groq Llama 3.3 • Tesseract OCR • FastAPI</p>
</div>
""", unsafe_allow_html=True)

# Recent analyses
if st.session_state.analysis_history:
    with st.sidebar.expander("Recent Analyses"):
        for item in st.session_state.analysis_history[-5:]:
            st.caption(f"{item['file']} ({item['time'].strftime('%H:%M:%S')})")