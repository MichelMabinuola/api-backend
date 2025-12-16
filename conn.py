from pymilvus import (
    Collection, FieldSchema, CollectionSchema,
    DataType, MilvusClient
)
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')

MILVUS_URI = os.getenv("MILVUS_URI")
MILVUS_TOKEN = os.getenv("MILVUS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

milvus_client = MilvusClient(
    uri=MILVUS_URI,
    token=MILVUS_TOKEN
)


def embed(text: str) -> list[float]:
    """
    Embed text using OpenAI's embedding model.
    
    Args:
        text (str): The text to embed.
    Returns:
        list[float]: Embedding vector.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input to embed() must be a non-empty string.")

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    except Exception as e:
        print(f"[Error] Failed to generate embedding: {e}")
        raise