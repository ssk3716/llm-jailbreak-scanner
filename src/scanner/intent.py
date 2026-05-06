import json
import os
import numpy as np
from typing import List, Optional
from sentence_transformers import SentenceTransformer

class IntentLayer:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', blacklist_path: Optional[str] = None):
        self.model = SentenceTransformer(model_name)
        if blacklist_path is None:
            # Default path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            blacklist_path = os.path.join(current_dir, 'vector_blacklist.json')
        
        with open(blacklist_path, 'r') as f:
            self.blacklist_concepts = json.load(f)
        
        # Pre-compute embeddings for the blacklist
        self.blacklist_embeddings = self.model.encode(self.blacklist_concepts)

    def calculate_similarity(self, text: str) -> float:
        """Calculates the maximum cosine similarity against the blacklist."""
        if not text.strip():
            return 0.0
            
        input_embedding = self.model.encode([text])
        
        # Cosine similarity: (A . B) / (||A|| * ||B||)
        # SentenceTransformer encode returns normalized vectors by default if requested, 
        # but we'll do it manually to be safe or use np.dot on normalized vectors.
        
        norms_input = np.linalg.norm(input_embedding, axis=1, keepdims=True)
        norms_blacklist = np.linalg.norm(self.blacklist_embeddings, axis=1, keepdims=True)
        
        input_norm = input_embedding / norms_input
        blacklist_norm = self.blacklist_embeddings / norms_blacklist
        
        similarities = np.dot(input_norm, blacklist_norm.T)[0]
        return float(np.max(similarities))

    def scan(self, text: str, threshold: float = 0.85) -> bool:
        """Flags text if semantic similarity exceeds threshold."""
        max_sim = self.calculate_similarity(text)
        return max_sim > threshold
