import os
from qdrant_client import QdrantClient

# Używamy qdrant_client.models żeby nie konflikotwało
import qdrant_client.http.models as models
from llm_client import generate_response
import requests

def get_embedding(text: str, get_secret_func) -> list:
    """Tworzy embedding za pomoca OpenAI (text-embedding-3-small)"""
    api_key = get_secret_func("OPENAI_API_KEY")
    if not api_key:
        print("Brak OPENAI_API_KEY do wektoryzacji. RAG zignorowany.")
        # Zwracamy dummy wektor żeby uniknąć crasha
        return [0.0] * 1536
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": text,
        "model": "text-embedding-3-small"
    }
    resp = requests.post("https://api.openai.com/v1/embeddings", headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["data"][0]["embedding"]

def query_rag(query: str, collection_name: str, qdrant_client: QdrantClient, get_secret_func, top_k: int = 3) -> list:
    """Zapytanie RAG do wskazanej kolekcji (domyślnie 'constraints' lub 'checkpoints')"""
    if qdrant_client is None:
        return ["RAG OFFLINE: QdrantClient = None"]
        
    try:
        vector = get_embedding(query, get_secret_func)
        results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=top_k
        )
        return [p.payload.get("text", "") for p in results]
    except Exception as e:
        print(f"⚠️ RAG Query Error: {e}")
        return [f"Błąd wektoryzacji: {e}"]
