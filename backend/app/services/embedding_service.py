from huggingface_hub import InferenceClient
import numpy as np
from ..config import HF_API_KEY

# HuggingFace Inference Client - handles routing automatically to correct endpoints
client = InferenceClient(token=HF_API_KEY)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def get_embedding(text: str, max_retries: int = 3):
    """
    Generate embeddings for a given text using HuggingFace Inference API.
    Uses InferenceClient which automatically routes to correct endpoints.
    """
    if not text or not text.strip():
        raise ValueError("Text input cannot be empty")
    
    try:
        # Use sentence_similarity task for embeddings
        embedding = client.feature_extraction(text, model=MODEL_NAME)
        
        # Handle different response formats
        if isinstance(embedding, np.ndarray):
            return embedding.flatten().tolist()
        elif isinstance(embedding, list):
            # If it's a nested list (batch), flatten appropriately
            if embedding and isinstance(embedding[0], list):
                # For nested lists, take the mean or first element based on structure
                if len(embedding) == 1:
                    return embedding[0]
                # Mean pooling across token embeddings
                return np.mean(embedding, axis=0).tolist()
            return embedding
        else:
            raise ValueError(f"Unexpected embedding format: {type(embedding)}")
            
    except Exception as e:
        error_msg = f"HuggingFace API error: {str(e)}"
        raise Exception(error_msg)

