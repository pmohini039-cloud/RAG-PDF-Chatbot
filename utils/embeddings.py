from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    """
    Returns the embedding model used for vector search.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )

    return embeddings