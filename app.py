#!/usr/bin/env python3
"""
File Converter - Streamlit Web GUI
A simple web interface for converting documents between formats.
"""

import streamlit as st
import tempfile
from pathlib import Path
from converter import DocumentConverter, ImageConverter

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
st.markdown("Convert documents and images between common formats instantly.")

# Initialize converters
converter = DocumentConverter()
image_converter = ImageConverter()

# Format options for documents
DOC_INPUT_FORMATS = ['.txt', '.docx', '.pdf', '.rtf', '.odt', '.html', '.md']
DOC_OUTPUT_FORMATS = ['.txt', '.docx', '.pdf', '.rtf', '.odt', '.html', '.md']

# Format options for images
IMG_INPUT_FORMATS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico']
IMG_OUTPUT_FORMATS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.ico']

# Tabs for different conversion types
tab_docs, tab_images = st.tabs(["📄 Documents", "🖼️ Images"])

# ===== DOCUMENT CONVERSION TAB =====
with tab_docs:
    # File upload
    doc_uploaded_file = st.file_uploader(
        "Drop your document here or click to browse",
        type=[fmt.strip('.') for fmt in DOC_INPUT_FORMATS],
        help="Supported formats: TXT, DOCX, PDF, RTF, ODT, HTML, MD",
        key="doc_uploader"
    )

    if doc_uploaded_file:
        # Show file info
        file_ext = Path(doc_uploaded_file.name).suffix.lower()
        st.info(f"**Uploaded:** {doc_uploaded_file.name} ({doc_uploaded_file.size / 1024:.1f} KB)")
        
        # Output format selector
        col1, col2 = st.columns([2, 1])
        with col1:
            # Filter out the input format from output options
            available_outputs = [fmt for fmt in DOC_OUTPUT_FORMATS if fmt != file_ext]
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
                }.get(x, x),
                key="doc_output_format"
            )
        
        # Convert button
        if st.button("🔄 Convert Document", type="primary", use_container_width=True, key="doc_convert"):
            with st.spinner("Converting..."):
                try:
                    # Save uploaded file to temp location with original name
                    tmp_dir = tempfile.mkdtemp()
                    tmp_input_path = Path(tmp_dir) / doc_uploaded_file.name
                    tmp_input_path.write_bytes(doc_uploaded_file.getvalue())
                    
                    # Perform conversion
                    output_path = converter.convert(str(tmp_input_path), output_format)
                    
                    # Read the converted file
                    with open(output_path, 'rb') as f:
                        converted_data = f.read()
                    
                    # Success message
                    st.success("✅ Conversion complete!")
                    
                    # Download button
                    output_filename = Path(doc_uploaded_file.name).stem + output_format
                    st.download_button(
                        label=f"⬇️ Download {output_filename}",
                        data=converted_data,
                        file_name=output_filename,
                        mime="application/octet-stream",
                        use_container_width=True,
                        key="doc_download"
                    )
                    
                    # Also show where it was saved locally
                    st.caption(f"Also saved to: {output_path}")
                    
                    # Cleanup temp files
                    Path(tmp_input_path).unlink(missing_ok=True)
                    Path(tmp_dir).rmdir()
                    
                except Exception as e:
                    st.error(f"❌ Conversion failed: {str(e)}")

# ===== IMAGE CONVERSION TAB =====
with tab_images:
    # File upload
    img_uploaded_file = st.file_uploader(
        "Drop your image here or click to browse",
        type=[fmt.strip('.') for fmt in IMG_INPUT_FORMATS],
        help="Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF, WebP, ICO",
        key="img_uploader"
    )

    if img_uploaded_file:
        # Show file info and preview
        file_ext = Path(img_uploaded_file.name).suffix.lower()
        st.info(f"**Uploaded:** {img_uploaded_file.name} ({img_uploaded_file.size / 1024:.1f} KB)")
        
        # Show image preview
        col_preview, col_options = st.columns([1, 1])
        with col_preview:
            st.image(img_uploaded_file, caption="Preview", use_container_width=True)
        
        with col_options:
            # Output format selector
            available_outputs = [fmt for fmt in IMG_OUTPUT_FORMATS if fmt != file_ext and fmt != '.jpeg' or (fmt == '.jpeg' and file_ext not in ['.jpg', '.jpeg'])]
            # Remove duplicate jpeg/jpg
            if file_ext in ['.jpg', '.jpeg']:
                available_outputs = [fmt for fmt in available_outputs if fmt not in ['.jpg', '.jpeg']]
            
            img_output_format = st.selectbox(
                "Convert to:",
                available_outputs,
                format_func=lambda x: {
                    '.png': 'PNG (.png)',
                    '.jpg': 'JPEG (.jpg)',
                    '.jpeg': 'JPEG (.jpeg)',
                    '.gif': 'GIF (.gif)',
                    '.bmp': 'Bitmap (.bmp)',
                    '.tiff': 'TIFF (.tiff)',
                    '.webp': 'WebP (.webp)',
                    '.ico': 'Icon (.ico)'
                }.get(x, x),
                key="img_output_format"
            )
            
            # Quality slider for JPEG/WebP
            img_quality = 95
            if img_output_format in ['.jpg', '.jpeg', '.webp']:
                img_quality = st.slider("Quality", 1, 100, 95, key="img_quality",
                                        help="Higher values = better quality, larger file size")
        
        # Convert button
        if st.button("🔄 Convert Image", type="primary", use_container_width=True, key="img_convert"):
            with st.spinner("Converting..."):
                try:
                    # Save uploaded file to temp location with original name
                    tmp_dir = tempfile.mkdtemp()
                    tmp_input_path = Path(tmp_dir) / img_uploaded_file.name
                    tmp_input_path.write_bytes(img_uploaded_file.getvalue())
                    
                    # Perform conversion
                    output_path = image_converter.convert(
                        str(tmp_input_path), 
                        img_output_format,
                        quality=img_quality
                    )
                    
                    # Read the converted file
                    with open(output_path, 'rb') as f:
                        converted_data = f.read()
                    
                    # Success message
                    st.success("✅ Conversion complete!")
                    
                    # Show converted file size
                    st.caption(f"Converted file size: {len(converted_data) / 1024:.1f} KB")
                    
                    # MIME types for images
                    mime_types = {
                        '.png': 'image/png',
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.gif': 'image/gif',
                        '.bmp': 'image/bmp',
                        '.tiff': 'image/tiff',
                        '.webp': 'image/webp',
                        '.ico': 'image/x-icon'
                    }
                    
                    # Download button
                    output_filename = Path(img_uploaded_file.name).stem + img_output_format
                    st.download_button(
                        label=f"⬇️ Download {output_filename}",
                        data=converted_data,
                        file_name=output_filename,
                        mime=mime_types.get(img_output_format, 'application/octet-stream'),
                        use_container_width=True,
                        key="img_download"
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
    st.markdown("### 📄 Document Formats")
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
    
    st.markdown("### 🖼️ Image Formats")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        **Input Formats:**
        - `.png` - PNG
        - `.jpg/.jpeg` - JPEG
        - `.gif` - GIF
        - `.bmp` - Bitmap
        - `.tiff/.tif` - TIFF
        - `.webp` - WebP
        - `.ico` - Icon
        """)
    with col4:
        st.markdown("""
        **Output Formats:**
        - `.png` - PNG
        - `.jpg/.jpeg` - JPEG
        - `.gif` - GIF
        - `.bmp` - Bitmap
        - `.tiff` - TIFF
        - `.webp` - WebP
        - `.ico` - Icon
        """)
