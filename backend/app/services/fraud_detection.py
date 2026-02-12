"""
Advanced Fraud Detection System
Multi-level resume duplication and anomaly detection
"""
from ..config import SIMILARITY_THRESHOLD
from ..utils.similarity import cosine_similarity
from typing import List, Dict, Tuple
import re


class FraudDetector:
    """Advanced fraud detection with multiple checks"""
    
    def __init__(self):
        self.similarity_threshold = SIMILARITY_THRESHOLD
        self.high_risk_threshold = 0.92
        self.medium_risk_threshold = 0.85
    
    def compute_similarity(self, new_emb: List[float], all_embeddings: List[List[float]]) -> Tuple[float, int]:
        """
        Compute maximum similarity against all existing resumes
        
        Returns:
            Tuple of (max_similarity, index_of_most_similar)
        """
        if not all_embeddings:
            return 0.0, -1
        
        max_sim = 0.0
        max_index = -1
        
        for idx, emb in enumerate(all_embeddings):
            sim = cosine_similarity(new_emb, emb)
            if sim > max_sim:
                max_sim = sim
                max_index = idx
        
        return round(max_sim, 4), max_index
    
    def detect_text_duplication(self, new_text: str, existing_texts: List[str]) -> Dict:
        """
        Check for exact or near-exact text duplication
        More sensitive than embedding similarity
        """
        if not existing_texts:
            return {
                "has_duplication": False,
                "max_text_similarity": 0.0,
                "duplicate_index": -1
            }
        
        # Normalize text for comparison
        new_normalized = self._normalize_text(new_text)
        
        max_similarity = 0.0
        duplicate_index = -1
        
        for idx, existing_text in enumerate(existing_texts):
            existing_normalized = self._normalize_text(existing_text)
            
            # Compute character-level similarity
            similarity = self._text_similarity(new_normalized, existing_normalized)
            
            if similarity > max_similarity:
                max_similarity = similarity
                duplicate_index = idx
        
        return {
            "has_duplication": max_similarity > 0.90,
            "max_text_similarity": round(max_similarity, 4),
            "duplicate_index": duplicate_index,
            "risk_level": self._get_text_risk_level(max_similarity)
        }
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        # Remove extra whitespace and convert to lowercase
        text = re.sub(r'\s+', ' ', text.lower())
        # Remove special characters but keep letters and numbers
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return text.strip()
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Compute character-level similarity using Jaccard index"""
        if not text1 or not text2:
            return 0.0
        
        # Split into character n-grams (3-grams)
        n = 3
        ngrams1 = set(text1[i:i+n] for i in range(len(text1)-n+1))
        ngrams2 = set(text2[i:i+n] for i in range(len(text2)-n+n))
        
        if not ngrams1 or not ngrams2:
            return 0.0
        
        intersection = len(ngrams1.intersection(ngrams2))
        union = len(ngrams1.union(ngrams2))
        
        return intersection / union if union > 0 else 0.0
    
    def check_email_duplication(self, email: str, existing_emails: List[str]) -> bool:
        """Check if email already exists"""
        return email.lower() in [e.lower() for e in existing_emails]
    
    def detect_template_usage(self, text: str) -> Dict:
        """
        Detect if resume appears to be from a common template
        Common indicators: repeated phrases, generic wording
        """
        text_lower = text.lower()
        
        # Common template phrases
        template_phrases = [
            "curriculum vitae",
            "professional summary",
            "objective statement",
            "references available upon request",
            "detail-oriented professional",
            "results-driven",
            "proven track record",
            "team player"
        ]
        
        phrase_count = sum(1 for phrase in template_phrases if phrase in text_lower)
        
        # Generic content indicators
        generic_indicators = [
            "insert name here",
            "your name",
            "[name]",
            "lorem ipsum",
            "sample text"
        ]
        
        has_placeholder = any(indicator in text_lower for indicator in generic_indicators)
        
        template_score = min(phrase_count / len(template_phrases), 1.0)
        
        return {
            "appears_templated": template_score > 0.4 or has_placeholder,
            "template_score": round(template_score, 4),
            "has_placeholder": has_placeholder,
            "generic_phrase_count": phrase_count
        }
    
    def _get_text_risk_level(self, similarity: float) -> str:
        """Determine risk level based on text similarity"""
        if similarity >= 0.95:
            return "critical"
        elif similarity >= 0.90:
            return "high"
        elif similarity >= 0.80:
            return "medium"
        else:
            return "low"
    
    def _get_embedding_risk_level(self, similarity: float) -> str:
        """Determine risk level based on embedding similarity"""
        if similarity >= self.high_risk_threshold:
            return "high"
        elif similarity >= self.medium_risk_threshold:
            return "medium"
        elif similarity >= self.similarity_threshold:
            return "low"
        else:
            return "none"
    
    def comprehensive_fraud_check(
        self, 
        new_embedding: List[float],
        new_text: str,
        new_email: str,
        existing_embeddings: List[List[float]],
        existing_texts: List[str],
        existing_emails: List[str]
    ) -> Dict:
        """
        Perform comprehensive fraud detection checks
        
        Returns:
            Complete fraud analysis report
        """
        # Embedding similarity check
        emb_sim, similar_index = self.compute_similarity(new_embedding, existing_embeddings)
        
        # Text duplication check
        text_dup = self.detect_text_duplication(new_text, existing_texts)
        
        # Email duplication check
        email_dup = self.check_email_duplication(new_email, existing_emails)
        
        # Template detection
        template_check = self.detect_template_usage(new_text)
        
        # Overall fraud determination
        fraud_flag = (
            emb_sim > self.similarity_threshold or
            text_dup["has_duplication"] or
            email_dup or
            template_check["has_placeholder"]
        )
        
        # Risk level determination
        risk_factors = []
        if emb_sim > self.high_risk_threshold:
            risk_factors.append("high_embedding_similarity")
        if text_dup["has_duplication"]:
            risk_factors.append("text_duplication")
        if email_dup:
            risk_factors.append("email_duplication")
        if template_check["has_placeholder"]:
            risk_factors.append("template_placeholder")
        
        overall_risk = "high" if len(risk_factors) >= 2 else \
                      "medium" if len(risk_factors) == 1 else \
                      "low"
        
        return {
            "fraud_flag": fraud_flag,
            "overall_risk": overall_risk,
            "risk_factors": risk_factors,
            "similarity_index": emb_sim,
            "embedding_risk": self._get_embedding_risk_level(emb_sim),
            "text_duplication": text_dup,
            "email_duplication": email_dup,
            "template_check": template_check,
            "similar_resume_index": similar_index,
            "requires_review": overall_risk in ["high", "medium"] or emb_sim > self.high_risk_threshold
        }


# Singleton instance
fraud_detector = FraudDetector()


def compute_similarity(new_emb: List[float], all_embeddings: List[List[float]]) -> float:
    """Compute maximum similarity (backward compatible)"""
    sim, _ = fraud_detector.compute_similarity(new_emb, all_embeddings)
    return sim


def detect_fraud(sim_index: float) -> bool:
    """Simple fraud detection (backward compatible)"""
    return sim_index > SIMILARITY_THRESHOLD


def comprehensive_fraud_analysis(
    new_embedding: List[float],
    new_text: str,
    new_email: str,
    existing_candidates: List
) -> Dict:
    """
    Perform comprehensive fraud detection
    
    Args:
        new_embedding: Resume embedding vector
        new_text: Resume text
        new_email: Candidate email
        existing_candidates: List of existing candidate records
        
    Returns:
        Comprehensive fraud report
    """
    existing_embeddings = [c.resume_embedding for c in existing_candidates]
    existing_texts = [c.resume_text for c in existing_candidates]
    existing_emails = [c.email for c in existing_candidates]
    
    return fraud_detector.comprehensive_fraud_check(
        new_embedding,
        new_text,
        new_email,
        existing_embeddings,
        existing_texts,
        existing_emails
    )

