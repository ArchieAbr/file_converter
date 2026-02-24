import os
from pathlib import Path
from typing import Optional
from docx import Document as DocxDocument
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

try:
    pass
except ImportError:
    print("Install required packages: python-docx pdf2image pillow pytesseract")


class DocumentConverter:
    """Convert between various document formats."""
    
    SUPPORTED_FORMATS = {'.txt', '.docx', '.pdf', '.png', '.jpg', '.jpeg'}
    
    def __init__(self):
        self.output_dir = Path.home() / "Desktop" / "Converted Documents"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def convert(self, input_path: str, output_format: str) -> Optional[str]:
        """Convert a document to the specified format."""
        input_file = Path(input_path)
        
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {input_path}")
        
        input_format = input_file.suffix.lower()
        output_format = output_format.lower()
        
        if not output_format.startswith('.'):
            output_format = f'.{output_format}'
        
        if output_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {output_format}")
        
        # Read content based on input format
        content = self._read_file(input_file, input_format)
        
        # Write content based on output format
        output_path = self.output_dir / f"{input_file.stem}{output_format}"
        self._write_file(output_path, content, output_format)
        
        return str(output_path)
    
    def _read_file(self, file_path: Path, file_format: str) -> str:
        """Read document content."""
        if file_format == '.txt':
            return file_path.read_text(encoding='utf-8')
        elif file_format == '.docx':
            doc = DocxDocument(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_format == '.pdf':
            return self._extract_pdf_text(file_path)
        else:
            raise ValueError(f"Cannot read format: {file_format}")
    
    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF using OCR."""
        images = convert_from_path(file_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
        return text
    
    def _write_file(self, output_path: Path, content: str, file_format: str) -> None:
        """Write content to file."""
        if file_format == '.txt':
            output_path.write_text(content, encoding='utf-8')
        elif file_format == '.docx':
            doc = DocxDocument()
            doc.add_paragraph(content)
            doc.save(output_path)
        else:
            raise ValueError(f"Cannot write format: {file_format}")


if __name__ == "__main__":
    converter = DocumentConverter()
    # Example: converter.convert("sample.pdf", ".txt")