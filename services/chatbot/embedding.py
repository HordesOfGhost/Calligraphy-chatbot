from typing import List
from huggingface_hub import InferenceClient
import numpy as np

class HFMiniLMEmbeddings:
    def __init__(self, hf_token: str):
        self.client = InferenceClient(api_key=hf_token)
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"

    def mean_pooling(self, token_embeddings):
        # If token_embeddings is a flat vector (list of floats or numpy array 1D), just return it as is
        # This covers the case when feature_extraction returns an embedding vector for the whole sentence
        if isinstance(token_embeddings[0], (float, np.floating)):
            return token_embeddings

        # Otherwise, token_embeddings is list of token embeddings; do mean pooling
        length = len(token_embeddings)
        dim = len(token_embeddings[0])
        pooled = [0.0] * dim
        for token_emb in token_embeddings:
            for i in range(dim):
                pooled[i] += token_emb[i]
        pooled = [x / length for x in pooled]
        return pooled


    def embed_documents(self, texts):
        all_embeddings = []
        for text in texts:
            token_embs = self.client.feature_extraction(text, model=self.model_name)
            # If token_embs is already a vector, return directly
            if isinstance(token_embs[0], float):
                all_embeddings.append(token_embs)
            else:
                pooled_emb = self.mean_pooling(token_embs)
                all_embeddings.append(pooled_emb)
        return all_embeddings

    def embed_query(self, text):
        token_embs = self.client.feature_extraction(text, model=self.model_name)
        if isinstance(token_embs[0], float):
            return token_embs
        return self.mean_pooling(token_embs)

    def __call__(self, texts):
        # This makes your object callable, so FAISS.from_texts works
        if isinstance(texts, str):
            return self.embed_query(texts)
        elif isinstance(texts, list):
            return self.embed_documents(texts)
        else:
            raise ValueError("Input must be str or list of str")
