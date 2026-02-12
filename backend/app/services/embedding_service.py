import requests
import numpy as np
from ..config import HF_API_KEY

# HuggingFace API configuration with updated endpoint
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

def get_embedding(text: str, max_retries: int = 3):
    """
    Generate embeddings for a given text using HuggingFace Inference API.
    Uses the updated HuggingFace API endpoint.
    """
    if not text or not text.strip():
        raise ValueError("Text input cannot be empty")
    
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": text,
        "options": {"wait_for_model": True}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            embedding = response.json()
            
            # Handle different response formats
            if isinstance(embedding, np.ndarray):
                return embedding.tolist()
            elif isinstance(embedding, list):
                # If it's a nested list (batch), take the first element
                if embedding and isinstance(embedding[0], list):
                    return embedding[0]
                return embedding
            else:
                raise ValueError(f"Unexpected embedding format: {type(embedding)}")
        else:
            error_msg = f"HuggingFace API error (Status {response.status_code}): {response.text}"
            raise Exception(error_msg)
            
    except requests.exceptions.RequestException as e:
        error_msg = f"HuggingFace API request error: {str(e)}"
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f"HuggingFace API error: {str(e)}"
        raise Exception(error_msg)

