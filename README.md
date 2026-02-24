# File Converter

> Version 1.1

A document converter that can convert between commonly used file formats natively on device.

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
