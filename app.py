#!/usr/bin/env python3
"""
File Converter - Streamlit Web GUI
A simple web interface for converting documents between formats.
"""

import streamlit as st
import tempfile
from pathlib import Path
from converter import DocumentConverter

# Page configuration
st.set_page_config(
    page_title="File Converter",
    page_icon="📄",
    layout="centered"
)

# Custom CSS for clean look
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📄 File Converter")
st.markdown("Convert documents between common formats instantly.")

# Initialize converter
converter = DocumentConverter()

# Format options
INPUT_FORMATS = ['.txt', '.docx', '.pdf', '.rtf', '.odt', '.html', '.md']
OUTPUT_FORMATS = ['.txt', '.docx', '.pdf', '.rtf', '.odt', '.html', '.md']

# File upload
uploaded_file = st.file_uploader(
    "Drop your file here or click to browse",
    type=[fmt.strip('.') for fmt in INPUT_FORMATS],
    help="Supported formats: TXT, DOCX, PDF, RTF, ODT, HTML, MD"
)

if uploaded_file:
    # Show file info
    file_ext = Path(uploaded_file.name).suffix.lower()
    st.info(f"**Uploaded:** {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
    
    # Output format selector
    col1, col2 = st.columns([2, 1])
    with col1:
        # Filter out the input format from output options
        available_outputs = [fmt for fmt in OUTPUT_FORMATS if fmt != file_ext]
        output_format = st.selectbox(
            "Convert to:",
            available_outputs,
            format_func=lambda x: {
                '.txt': 'Plain Text (.txt)',
                '.docx': 'Word Document (.docx)',
                '.pdf': 'PDF (.pdf)',
                '.rtf': 'Rich Text (.rtf)',
                '.odt': 'OpenDocument (.odt)',
                '.html': 'HTML (.html)',
                '.md': 'Markdown (.md)'
            }.get(x, x)
        )
    
    # Convert button
    if st.button("🔄 Convert", type="primary", use_container_width=True):
        with st.spinner("Converting..."):
            try:
                # Save uploaded file to temp location with original name
                tmp_dir = tempfile.mkdtemp()
                tmp_input_path = Path(tmp_dir) / uploaded_file.name
                tmp_input_path.write_bytes(uploaded_file.getvalue())
                
                # Perform conversion
                output_path = converter.convert(str(tmp_input_path), output_format)
                
                # Read the converted file
                with open(output_path, 'rb') as f:
                    converted_data = f.read()
                
                # Success message
                st.success("✅ Conversion complete!")
                
                # Download button
                output_filename = Path(uploaded_file.name).stem + output_format
                st.download_button(
                    label=f"⬇️ Download {output_filename}",
                    data=converted_data,
                    file_name=output_filename,
                    mime="application/octet-stream",
                    use_container_width=True
                )
                
                # Also show where it was saved locally
                st.caption(f"Also saved to: {output_path}")
                
                # Cleanup temp files
                Path(tmp_input_path).unlink(missing_ok=True)
                Path(tmp_dir).rmdir()
                
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")

# Footer with supported formats
with st.expander("ℹ️ Supported Formats"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Input Formats:**
        - `.txt` - Plain text
        - `.docx` - Word document
        - `.pdf` - PDF (via OCR)
        - `.rtf` - Rich text
        - `.odt` - OpenDocument
        - `.html` - HTML
        - `.md` - Markdown
        """)
    with col2:
        st.markdown("""
        **Output Formats:**
        - `.txt` - Plain text
        - `.docx` - Word document
        - `.pdf` - PDF
        - `.rtf` - Rich text
        - `.odt` - OpenDocument
        - `.html` - HTML
        - `.md` - Markdown
        """)
