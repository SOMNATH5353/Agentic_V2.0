import PyPDF2
from io import BytesIO
from typing import Dict, Any
from ..utils.text_cleaner import clean_text

def parse_jd_pdf(pdf_content: bytes) -> Dict[str, Any]:
    """
    Parse Job Description from PDF file
    
    Args:
        pdf_content: PDF file content as bytes
        
    Returns:
        Dictionary containing parsed JD information
    """
    try:
        pdf_file = BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text() + "\n"
        
        # Clean the extracted text to remove NUL bytes and control characters
        full_text = clean_text(full_text)
        
        return {
            "jd_text": full_text,
            "page_count": len(pdf_reader.pages),
            "success": True
        }
    except Exception as e:
        return {
            "jd_text": "",
            "error": str(e),
            "success": False
        }
