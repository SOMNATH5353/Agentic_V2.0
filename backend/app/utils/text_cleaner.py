import re
from typing import Optional


def clean_text(text: Optional[str]) -> str:
    """
    Clean text by removing problematic characters for database storage.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text safe for database storage
    """
    if not text:
        return ""
    
    # Remove NUL (0x00) bytes - these cause database errors
    text = text.replace('\x00', '')
    
    # Remove other control characters except common whitespace
    # Keep: newline (\n), carriage return (\r), tab (\t)
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Normalize whitespace (optional, but helps with consistency)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def clean_dict_strings(data: dict) -> dict:
    """
    Recursively clean all string values in a dictionary.
    
    Args:
        data: Dictionary with potentially unclean strings
        
    Returns:
        Dictionary with cleaned strings
    """
    cleaned = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned[key] = clean_text(value)
        elif isinstance(value, dict):
            cleaned[key] = clean_dict_strings(value)
        elif isinstance(value, list):
            cleaned[key] = [
                clean_text(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            cleaned[key] = value
    return cleaned
