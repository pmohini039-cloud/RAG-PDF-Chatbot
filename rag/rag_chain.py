from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from config import GROQ_API_KEY
from utils.retriever import get_retriever


PROMPT = """
You are an intelligent AI Research Assistant.

Answer the user's question using ONLY the provided context.

If the answer is not present in the context, simply say:

"I couldn't find that information in the provided documents."

Do not make up information.

Context:
{context}

Question:
{input}

Answer:
"""


def format_docs(documents):
    """
    Combines retrieved documents into a single context string.
    """
    return "\n\n".join(doc.page_content for doc in documents)


def create_rag_chain(collection_name):
    """
    Creates the complete RAG pipeline.

    Returns:
        retriever
        rag_chain
    """

    retriever = get_retriever(collection_name)

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_template(PROMPT)

    rag_chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return retriever, rag_chain