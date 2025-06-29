from typing import List
from huggingface_hub import InferenceClient
import numpy as np

class HFMiniLMEmbeddings:
    """
    A wrapper class for embedding text using the MiniLM model hosted on Hugging Face Inference API.
    It supports both single query embedding and batch document embedding.
    """
    def __init__(self, hf_token: str):
        """
        Initialize the Hugging Face Inference Client.

        Args:
            hf_token (str): Hugging Face API token for authentication.
        """
        self.client = InferenceClient(api_key=hf_token)
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"

    def mean_pooling(self, token_embeddings):
        """
        Perform mean pooling on token embeddings to obtain a single sentence-level embedding.

        Args:
            token_embeddings (List[List[float]] or List[float]): Token-level embeddings or a single vector.

        Returns:
            List[float]: Sentence-level embedding vector.
        """
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
        """
        Embed a list of documents using MiniLM and mean pooling.

        Args:
            texts (List[str]): List of input texts to embed.

        Returns:
            List[List[float]]: List of embedding vectors for each text.
        """
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
        """
        Embed a single query (string) using MiniLM.

        Args:
            text (str): The input query text.

        Returns:
            List[float]: The embedding vector.
        """
        token_embs = self.client.feature_extraction(text, model=self.model_name)
        if isinstance(token_embs[0], float):
            return token_embs
        return self.mean_pooling(token_embs)

    def __call__(self, texts):
        """
        Make the class instance callable. Automatically routes to embedding method based on input type.

        Args:
            texts (str or List[str]): A single string or a list of strings to embed.

        Returns:
            List[float] or List[List[float]]: Embedding vector(s).

        Raises:
            ValueError: If input is not a string or list of strings.
        """
        if isinstance(texts, str):
            return self.embed_query(texts)
        elif isinstance(texts, list):
            return self.embed_documents(texts)
        else:
            raise ValueError("Input must be str or list of str")
