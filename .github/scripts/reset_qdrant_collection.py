"""
Recria a coleção 'gus' no Qdrant com 384 dims (HuggingFace all-MiniLM-L6-v2).
Roda antes da migração quando há conflito de dimensão.
"""
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

COLLECTION = "gus"
EXPECTED_DIMS = 384


def main():
    client = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
    )

    existing = {c.name for c in client.get_collections().collections}

    if COLLECTION in existing:
        info = client.get_collection(COLLECTION)
        dims = info.config.params.vectors.size
        print(f"Coleção '{COLLECTION}' existe com {dims} dims.")
        if dims == EXPECTED_DIMS:
            print("Dimensão correta — nada a fazer.")
            return
        print(f"Dimensão errada ({dims} != {EXPECTED_DIMS}). Deletando...")
        client.delete_collection(COLLECTION)
        print("Deletada.")
    else:
        print(f"Coleção '{COLLECTION}' não existe.")

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=EXPECTED_DIMS, distance=Distance.COSINE),
    )
    print(f"Coleção '{COLLECTION}' recriada com {EXPECTED_DIMS} dims.")


if __name__ == "__main__":
    main()
