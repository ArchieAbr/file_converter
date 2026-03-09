#!/usr/bin/env python3
"""
File Converter CLI
Convert documents between txt, docx, and pdf formats.
"""

import sys
import argparse
from pathlib import Path
from converter import DocumentConverter, ImageConverter


def print_help():
    """Print usage instructions."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    FILE CONVERTER v3.0                       ║
╠══════════════════════════════════════════════════════════════╣
║  Convert documents and images between commonly used formats  ║
║                                                              ║
║  TIP: For a visual interface, run: streamlit run app.py      ║
║                                                              ║
║  SUPPORTED DOCUMENT FORMATS:                                 ║
║    Input:  .txt .docx .pdf .rtf .odt .html .md               ║
║    Output: .txt .docx .pdf .rtf .odt .html .md               ║
║                                                              ║
║  SUPPORTED IMAGE FORMATS:                                    ║
║    Input:  .png .jpg .jpeg .gif .bmp .tiff .tif .webp .ico   ║
║    Output: .png .jpg .jpeg .gif .bmp .tiff .webp .ico        ║
║                                                              ║
║  USAGE:                                                      ║
║    python convert.py <input_file> <output_format> [options]  ║
║                                                              ║
║  OPTIONS (images only):                                      ║
║    --quality <1-100>   JPEG/WebP quality (default: 95)       ║
║                                                              ║
║  EXAMPLES:                                                   ║
║    python convert.py document.pdf .txt                       ║
║    python convert.py notes.txt .docx                         ║
║    python convert.py photo.png .jpg --quality 85             ║
║    python convert.py image.webp .png                         ║
║                                                              ║
║  OUTPUT:                                                     ║
║    Documents: ~/Desktop/Converted Documents/                 ║
║    Images:    ~/Desktop/Converted Images/                    ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    parser = argparse.ArgumentParser(
        description="Convert documents and images between formats.",
        add_help=False
    )
    parser.add_argument("input_file", nargs="?", help="Path to the input file")
    parser.add_argument("output_format", nargs="?", help="Desired output format (e.g., .txt, .docx, .png, .jpg)")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    parser.add_argument("--quality", type=int, default=95, help="Image quality for JPEG/WebP (1-100, default: 95)")
    
    args = parser.parse_args()
    
    # Show help if requested or no arguments provided
    if args.help or not args.input_file:
        print_help()
        sys.exit(0)
    
    if not args.output_format:
        print("\n❌ Error: Please specify an output format.")
        print("   Example: python convert.py document.pdf .txt")
        print("   Example: python convert.py photo.png .jpg\n")
        sys.exit(1)
    
    # Validate input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"\n❌ Error: File not found: {args.input_file}\n")
        sys.exit(1)
    
    # Determine if this is an image or document conversion
    input_ext = input_path.suffix.lower()
    output_format = args.output_format.lower()
    if not output_format.startswith('.'):
        output_format = f'.{output_format}'
    
    # Image formats
    image_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico'}
    # Document formats
    doc_formats = {'.txt', '.docx', '.pdf', '.rtf', '.odt', '.html', '.htm', '.md'}
    
    # Perform conversion
    try:
        if input_ext in image_formats or output_format in image_formats:
            # Image conversion
            image_converter = ImageConverter()
            print(f"\n⏳ Converting image {input_path.name}...")
            output_path = image_converter.convert(
                args.input_file, 
                output_format,
                quality=args.quality
            )
            print(f"✅ Success! Image saved to:\n   {output_path}\n")
        elif input_ext in doc_formats or output_format in doc_formats:
            # Document conversion
            converter = DocumentConverter()
            print(f"\n⏳ Converting {input_path.name}...")
            output_path = converter.convert(args.input_file, output_format)
            print(f"✅ Success! File saved to:\n   {output_path}\n")
        else:
            print(f"\n❌ Error: Unsupported file format: {input_ext}\n")
            sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Conversion failed: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
