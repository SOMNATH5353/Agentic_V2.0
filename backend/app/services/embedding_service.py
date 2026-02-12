from huggingface_hub import InferenceClient
import numpy as np
from ..config import HF_API_KEY

# Initialize HuggingFace Inference Client
client = InferenceClient(token=HF_API_KEY)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def get_embedding(text: str, max_retries: int = 3):
    """
    Generate embeddings for a given text using HuggingFace Inference Client.
    Uses the official huggingface_hub library which handles endpoint routing automatically.
    """
    if not text or not text.strip():
        raise ValueError("Text input cannot be empty")
    
    try:
        # Use the feature_extraction method for embeddings
        embedding = client.feature_extraction(text, model=MODEL_NAME)
        
        # Handle different response formats
        if isinstance(embedding, np.ndarray):
            # Convert numpy array to list
            return embedding.tolist()
        elif isinstance(embedding, list):
            # If it's a nested list (batch), take the first element
            if embedding and isinstance(embedding[0], list):
                return embedding[0]
            return embedding
        else:
            raise ValueError(f"Unexpected embedding format: {type(embedding)}")
            
    except Exception as e:
        error_msg = f"HuggingFace API error: {str(e)}"
        raise Exception(error_msg)

