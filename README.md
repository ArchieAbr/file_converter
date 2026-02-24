# File Converter

> Version 2.0

A document converter with a **web-based GUI** that converts between commonly used file formats natively on device.

![File Converter](https://img.shields.io/badge/version-2.0-blue) ![Python](https://img.shields.io/badge/python-3.8+-green)

## Supported Formats

### Input Formats (Read)

- `.txt` - Plain text files
- `.docx` - Microsoft Word documents
- `.pdf` - PDF files (uses OCR)
- `.rtf` - Rich Text Format
- `.odt` - OpenDocument Text
- `.html` / `.htm` - HTML documents
- `.md` - Markdown files

### Output Formats (Write)

- `.txt` - Plain text files
- `.docx` - Microsoft Word documents
- `.pdf` - PDF files
- `.rtf` - Rich Text Format
- `.odt` - OpenDocument Text
- `.html` - HTML documents
- `.md` - Markdown files

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Install system dependencies:
   - **Tesseract OCR** - Required for PDF text extraction
   - **Poppler** - Required for PDF to image conversion

On macOS:

```bash
brew install tesseract poppler
```

On Ubuntu/Debian:

```bash
sudo apt-get install tesseract-ocr poppler-utils
```

## Usage

### Web GUI (Recommended)

Launch the web interface:

```bash
streamlit run app.py
```

This opens a browser window where you can:

1. Drag and drop files to upload
2. Select output format from dropdown
3. Click Convert and download the result

### Command Line

```bash
# Show help and instructions
python3 convert.py

# Convert PDF to text
python3 convert.py document.pdf .txt

# Convert text to Word document
python3 convert.py notes.txt .docx

# Convert Word to PDF
python3 convert.py report.docx .pdf

# Convert HTML to Markdown
python3 convert.py webpage.html .md

# Convert RTF to ODT
python3 convert.py document.rtf .odt
```

### Python Module

```python
from converter import DocumentConverter

converter = DocumentConverter()

# Convert PDF to text
converter.convert("document.pdf", ".txt")

# Convert text to Word document
converter.convert("notes.txt", ".docx")

# Convert Word to PDF
converter.convert("report.docx", ".pdf")

# Convert HTML to Markdown
converter.convert("webpage.html", ".md")
```

Converted files are saved to `~/Desktop/Converted Documents/`.

## Dependencies

- `python-docx` - Word document handling
- `pdf2image` - PDF to image conversion
- `Pillow` - Image processing
- `pytesseract` - OCR text extraction
- `fpdf2` - PDF creation
- `odfpy` - OpenDocument format support
- `striprtf` - RTF reading
- `beautifulsoup4` - HTML parsing
- `markdown` - Markdown processing
- `streamlit` - Web GUI framework
