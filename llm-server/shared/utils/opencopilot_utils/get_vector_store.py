import os
from langchain.vectorstores.pinecone import Pinecone

from langchain.vectorstores.qdrant import Qdrant
from langchain.vectorstores.base import VectorStore
from .store_type import StoreType
from .config import VECTOR_STORE_INDEX_NAME, PINECONE_TEXT_KEY
from .interfaces import StoreOptions
from .get_embeddings import get_embeddings
import qdrant_client


def get_vector_store(options: StoreOptions) -> VectorStore:
    """Gets the vector store for the given options."""
    vector_store: VectorStore
    embedding = get_embeddings()

    store_type = os.environ.get("STORE")

    if store_type != StoreType.QDRANT.value:
        raise ValueError("Invalid STORE environment variable value")

    client = qdrant_client.QdrantClient(
        url=os.environ["QDRANT_URL"],
        prefer_grpc=True,
        api_key=os.getenv("QDRANT_API_KEY", None),
    )

    return Qdrant(
        client, collection_name=options.namespace, embeddings=embedding
    )