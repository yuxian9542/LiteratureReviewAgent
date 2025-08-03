import pdfplumber
from typing import Optional

class PDFParser:
    def __init__(self):
        pass
    
    def extract_text(self, pdf_path: str) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    def extract_metadata(self, pdf_path: str) -> dict:
        """Extract basic metadata from PDF"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return {
                    'num_pages': len(pdf.pages),
                    'metadata': pdf.metadata or {}
                }
        except Exception:
            return {'num_pages': 0, 'metadata': {}}