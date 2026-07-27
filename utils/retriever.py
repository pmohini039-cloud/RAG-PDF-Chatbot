from langchain_community.vectorstores import Chroma

from config import CHROMA_DB_PATH
from utils.embeddings import get_embeddings


def get_retriever(collection_name):
    """
    Loads the Chroma collection created during document processing
    and returns a retriever.
    """

    embeddings = get_embeddings()

    vector_db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4,
        },
    )

    return retriever