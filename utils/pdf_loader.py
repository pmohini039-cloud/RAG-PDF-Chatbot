import tempfile

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(uploaded_files):
    """
    Loads uploaded PDF files and stores the original filename
    in each document's metadata.
    """

    documents = []

    for uploaded_file in uploaded_files:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:

            temp_file.write(uploaded_file.read())

            temp_path = temp_file.name

        loader = PyPDFLoader(temp_path)

        docs = loader.load()

        # Store original filename
        for doc in docs:
            doc.metadata["file_name"] = uploaded_file.name

        documents.extend(docs)

    return documents


def load_pdf_from_path(pdf_path):
    """
    Loads a PDF from a local path.
    """

    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

    file_name = pdf_path.split("\\")[-1].split("/")[-1]

    for doc in docs:
        doc.metadata["file_name"] = file_name

    return docs