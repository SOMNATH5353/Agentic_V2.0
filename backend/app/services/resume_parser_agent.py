import PyPDF2
from io import BytesIO
from typing import Dict, Any
import re
from ..utils.text_cleaner import clean_text

def parse_resume_pdf(pdf_content: bytes) -> Dict[str, Any]:
    """
    Parse Resume from PDF file
    
    Args:
        pdf_content: PDF file content as bytes
        
    Returns:
        Dictionary containing parsed resume information
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
        
        # Basic extraction (you can enhance this with more sophisticated parsing)
        parsed_data = {
            "resume_text": full_text,
            "page_count": len(pdf_reader.pages),
            "success": True
        }
        
        # Try to extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, full_text)
        if emails:
            parsed_data["extracted_email"] = clean_text(emails[0])
        
        # Try to extract phone
        phone_pattern = r'\+?[\d\s\-\(\)]{10,}'
        phones = re.findall(phone_pattern, full_text)
        if phones:
            parsed_data["extracted_phone"] = clean_text(phones[0].strip())
        
        return parsed_data
        
    except Exception as e:
        return {
            "resume_text": "",
            "error": str(e),
            "success": False
        }
