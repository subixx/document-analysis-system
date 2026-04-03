import streamlit as st
import requests
import base64
import json
from pathlib import Path

st.set_page_config(page_title="DocuMind AI", page_icon="📄", layout="wide")

st.title("🧠 DocuMind AI")
st.markdown("Intelligent Document Analysis & Extraction")
st.markdown("---")

with st.sidebar:
    st.markdown("### Configuration")
    
    BACKEND_URL = "https://documind-backend-v97h.onrender.com"
    
    api_url = st.text_input("Backend API URL", value=BACKEND_URL)
    api_key = st.text_input("API Key", value="sk_track2_987654321", type="password")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("Upload PDF, DOCX, or Images for AI analysis")

st.markdown("### 📂 Upload Document")

uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'png', 'jpg', 'jpeg'], label_visibility="collapsed")

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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File Name", file_name)
    with col2:
        st.metric("Size", f"{len(file_content)/1024:.1f} KB")
    with col3:
        st.metric("Type", file_type.upper())
    
    if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
        with st.spinner("AI is analyzing..."):
            try:
                file_base64 = base64.b64encode(file_content).decode('utf-8')
                
                response = requests.post(
                    f"{api_url}/api/document-analyze",
                    json={
                        "fileName": file_name,
                        "fileType": file_type,
                        "fileBase64": file_base64
                    },
                    headers={"x-api-key": api_key},
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Analysis Complete!")
                    
                    st.markdown("### 📝 Summary")
                    st.info(result["summary"])
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Document Type", result.get("document_type", "Unknown"))
                    with col_b:
                        st.metric("Sentiment", result.get("sentiment", "Neutral"))
                    with col_c:
                        st.metric("Confidence", result.get("confidence", "N/A").upper())
                    
                    if result.get("key_topics"):
                        st.markdown("### 🏷️ Key Topics")
                        st.write(", ".join(result["key_topics"]))
                    
                    entities = result.get("entities", {})
                    if any(entities.values()):
                        st.markdown("### 🔍 Extracted Entities")
                        if entities.get("people"):
                            st.markdown(f"**People:** {', '.join(entities['people'])}")
                        if entities.get("organizations"):
                            st.markdown(f"**Organizations:** {', '.join(entities['organizations'])}")
                        if entities.get("dates"):
                            st.markdown(f"**Dates:** {', '.join(entities['dates'])}")
                    
                    st.caption(f"🤖 Analyzed by: {result.get('analyzed_by', 'Unknown')}")
                    
                    st.download_button("📥 Download JSON", json.dumps(result, indent=2), f"{Path(file_name).stem}_analysis.json")
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
