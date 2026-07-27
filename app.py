import os
import streamlit as st

from utils.streamer import stream_text
from utils.pdf_loader import load_pdf, load_pdf_from_path
from utils.pdf_downloader import download_pdf
from utils.website_loader import load_website
from utils.chunker import split_documents
from utils.vector_store import create_vector_store
from rag.rag_chain import create_rag_chain

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI Research Assistant")

st.markdown("""
Upload PDF documents, Website URLs or PDF URLs and ask questions
about their content using Retrieval-Augmented Generation (RAG).
""")

if "processed" not in st.session_state:
    st.session_state.processed = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "collection_name" not in st.session_state:
    st.session_state.collection_name = None

with st.sidebar:

    st.header("📂 Document Source")

    source = st.radio(
        "Choose Source",
        [
            "Upload PDF",
            "Website URL",
            "PDF URL",
        ],
    )

    uploaded_files = None
    website_url = ""
    pdf_url = ""

    if source == "Upload PDF":

        uploaded_files = st.file_uploader(
            "Upload PDF Files",
            type="pdf",
            accept_multiple_files=True,
        )

    elif source == "Website URL":

        website_url = st.text_input(
            "Website URL",
            placeholder="https://docs.python.org/3/",
        )

    else:

        pdf_url = st.text_input(
            "PDF URL",
            placeholder="https://example.com/file.pdf",
        )

    st.divider()

    process_button = st.button(
        "📄 Process Documents",
        use_container_width=True,
    )

    clear_button = st.button(
        "🗑 Clear Chat",
        use_container_width=True,
    )

    if clear_button:

        st.session_state.messages = []

        st.rerun()

if process_button:

    with st.spinner("Processing documents..."):

        try:

            if source == "Upload PDF":

                if not uploaded_files:
                    st.warning("Please upload at least one PDF.")
                    st.stop()

                documents = load_pdf(uploaded_files)

            elif source == "Website URL":

                if website_url.strip() == "":
                    st.warning("Please enter a Website URL.")
                    st.stop()

                documents = load_website(website_url)

            else:

                if pdf_url.strip() == "":
                    st.warning("Please enter a PDF URL.")
                    st.stop()

                pdf_path = download_pdf(pdf_url)

                documents = load_pdf_from_path(pdf_path)

            chunks = split_documents(documents)

            collection_name = create_vector_store(chunks)

            st.session_state.collection_name = collection_name

            st.session_state.processed = True

            st.session_state.messages = []

            st.success("✅ Documents processed successfully!")

        except Exception as e:

            st.error(f"❌ {e}")

            st.stop()

if st.session_state.processed:

    retriever, rag_chain = create_rag_chain(
        st.session_state.collection_name
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and "references" in message
            ):

                st.markdown("---")

                st.markdown("### 📚 References")

                for ref in message["references"]:

                    st.markdown(ref)

    question = st.chat_input(
        "Ask a question about your documents..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        docs = retriever.invoke(question)

        with st.spinner("Thinking..."):

            answer = rag_chain.invoke(question)

        unique_sources = set()

        references = []
        
        for doc in docs:

            source = doc.metadata.get(
                "file_name",
                doc.metadata.get("source", "Website"),
            )

            source = os.path.basename(str(source))

            page = doc.metadata.get("page")

            key = (source, page)

            if key in unique_sources:
                continue

            unique_sources.add(key)

            ref_number = len(references) + 1

            if page is not None:

                reference = (
                    f"[{ref_number}] "
                    f"{source} • Page {page + 1}"
                )

            else:

                reference = (
                    f"[{ref_number}] "
                    f"{source}"
                )

            references.append(reference)

        assistant_message = {
            "role": "assistant",
            "content": answer,
            "references": references,
        }

        st.session_state.messages.append(
            assistant_message
        )

        with st.chat_message("assistant"):

            # ChatGPT-style streaming
            st.write_stream(stream_text(answer))

            if references:

                st.markdown("---")
                st.markdown("### 📚 References")

                for ref in references:

                    st.markdown(ref)

# ----------------------------------------------------
# Empty State
# ----------------------------------------------------

else:

    st.info(
        """
## 👋 Welcome to the AI Research Assistant

This application allows you to chat with your documents using
Retrieval-Augmented Generation (RAG).

### Supported Sources

- 📄 Upload one or more PDF files
- 🌐 Paste a Website URL
- 🔗 Paste a direct PDF URL

### Example Questions

- Explain user-defined functions.
- Summarize the document.
- What are the key points?
- Explain lambda functions.
- Compare built-in and user-defined functions.
- Give examples from the document.

### Workflow

1. Select a source.
2. Click **Process Documents**.
3. Ask questions in the chat.

Happy Learning! 🚀
"""
    )