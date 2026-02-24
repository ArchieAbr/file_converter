# File Converter

> Version 1.0

A document converter that can convert between commonly used file formats natively on device.

## Supported Formats

- `.txt` - Plain text files
- `.docx` - Microsoft Word documents
- `.pdf` - PDF files (read-only, uses OCR)
- `.png`, `.jpg`, `.jpeg` - Image files

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
```

### Python Module

```python
from converter import DocumentConverter

converter = DocumentConverter()

# Convert PDF to text
converter.convert("document.pdf", ".txt")

# Convert text to Word document
converter.convert("notes.txt", ".docx")
```

Converted files are saved to `~/Desktop/Converted Documents/`.

## Dependencies

- `python-docx` - Word document handling
- `pdf2image` - PDF to image conversion
- `Pillow` - Image processing
- `pytesseract` - OCR text extraction
