import uuid

from langchain_community.vectorstores import Chroma

from config import CHROMA_DB_PATH
from utils.embeddings import get_embeddings


def create_vector_store(chunks):
    """
    Creates a new Chroma collection for the current session.
    Returns the collection name.
    """

    embeddings = get_embeddings()

    # Generate a unique collection name
    collection_name = f"collection_{uuid.uuid4().hex}"

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
        collection_name=collection_name,
    )

    try:
        vector_db.persist()
    except Exception:
        pass

    return collection_name