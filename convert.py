#!/usr/bin/env python3
"""
File Converter CLI
Convert documents between txt, docx, and pdf formats.
"""

import sys
import argparse
from pathlib import Path
from converter import DocumentConverter


def print_help():
    """Print usage instructions."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    FILE CONVERTER v1.1                       ║
╠══════════════════════════════════════════════════════════════╣
║  Convert documents between commonly used file formats        ║
║                                                              ║
║  SUPPORTED INPUT FORMATS:                                    ║
║    • .txt   - Plain text files                               ║
║    • .docx  - Microsoft Word documents                       ║
║    • .pdf   - PDF files (extracted via OCR)                  ║
║    • .rtf   - Rich Text Format                               ║
║    • .odt   - OpenDocument Text                              ║
║    • .html  - HTML documents                                 ║
║    • .md    - Markdown files                                 ║
║                                                              ║
║  SUPPORTED OUTPUT FORMATS:                                   ║
║    • .txt   - Plain text files                               ║
║    • .docx  - Microsoft Word documents                       ║
║    • .pdf   - PDF files                                      ║
║    • .rtf   - Rich Text Format                               ║
║    • .odt   - OpenDocument Text                              ║
║    • .html  - HTML documents                                 ║
║    • .md    - Markdown files                                 ║
║                                                              ║
║  USAGE:                                                      ║
║    python convert.py <input_file> <output_format>            ║
║                                                              ║
║  EXAMPLES:                                                   ║
║    python convert.py document.pdf .txt                       ║
║    python convert.py notes.txt .docx                         ║
║    python convert.py report.docx .pdf                        ║
║    python convert.py webpage.html .md                        ║
║                                                              ║
║  OUTPUT:                                                     ║
║    Files are saved to: ~/Desktop/Converted Documents/        ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    parser = argparse.ArgumentParser(
        description="Convert documents between txt, docx, and pdf formats.",
        add_help=False
    )
    parser.add_argument("input_file", nargs="?", help="Path to the input file")
    parser.add_argument("output_format", nargs="?", help="Desired output format (e.g., .txt, .docx)")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    
    args = parser.parse_args()
    
    # Show help if requested or no arguments provided
    if args.help or not args.input_file:
        print_help()
        sys.exit(0)
    
    if not args.output_format:
        print("\n❌ Error: Please specify an output format.")
        print("   Example: python convert.py document.pdf .txt\n")
        sys.exit(1)
    
    # Validate input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"\n❌ Error: File not found: {args.input_file}\n")
        sys.exit(1)
    
    # Perform conversion
    try:
        converter = DocumentConverter()
        print(f"\n⏳ Converting {input_path.name}...")
        output_path = converter.convert(args.input_file, args.output_format)
        print(f"✅ Success! File saved to:\n   {output_path}\n")
    except ValueError as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Conversion failed: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
