import os
import streamlit as st

from utils.streamer import stream_text
from utils.chat_export import (
    export_chat_as_txt,
    export_chat_as_pdf,
)
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

# Initialize Session State
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "processed" not in st.session_state:
    st.session_state.processed = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "collection_name" not in st.session_state:
    st.session_state.collection_name = None

if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = {}


# Theme CSS Application
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
            .stApp { background-color: #0e1117; color: #ffffff; }
            .stChatMessage { background-color: #1a1c23; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
            .stApp { background-color: #f0f2f6; color: #31333F; }
            .stChatMessage { background-color: #ffffff; }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title("📚 AI Research Assistant")

st.markdown(
    """
Upload PDF documents, Website URLs or PDF URLs and ask questions
about their content using Retrieval-Augmented Generation (RAG).
"""
)

with st.sidebar:
    # Theme Switcher
    theme_choice = st.selectbox(
        "🌙/☀️ Select Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1,
    )
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.divider()
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

    # Document Statistics Panel
    if st.session_state.processed and st.session_state.doc_stats:
        st.divider()
        st.subheader("📊 Document Statistics")
        stats = st.session_state.doc_stats
        col1, col2 = st.columns(2)
        col1.metric("Total Chunks", stats.get("chunks", 0))
        col2.metric("Total Pages", stats.get("pages", "N/A"))
        st.caption(f"**Sources:** {stats.get('sources', 1)}")

    # Export Section
    if st.session_state.messages:
        st.divider()
        st.subheader("⬇ Export Options")

        txt_data = export_chat_as_txt(st.session_state.messages)
        st.download_button(
            "📄 Download Chat (TXT)",
            data=txt_data,
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True,
        )

        pdf_data = export_chat_as_pdf(st.session_state.messages)
        st.download_button(
            "📕 Download Chat (PDF)",
            data=pdf_data,
            file_name="chat_history.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        # Reference Export
        all_refs = []
        for m in st.session_state.messages:
            if "references" in m:
                all_refs.extend(m["references"])

        if all_refs:
            ref_txt = "\n".join(set(all_refs))
            st.download_button(
                "🔗 Download References (TXT)",
                data=ref_txt,
                file_name="references.txt",
                mime="text/plain",
                use_container_width=True,
            )


# Processing Logic
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

            # Extract document statistics
            unique_pages = {
                doc.metadata.get("page")
                for doc in documents
                if doc.metadata.get("page") is not None
            }
            num_pages = len(unique_pages) if unique_pages else "N/A"

            st.session_state.doc_stats = {
                "chunks": len(chunks),
                "pages": num_pages,
                "sources": len({doc.metadata.get("source", "Unknown") for doc in documents}),
            }

            st.session_state.collection_name = collection_name
            st.session_state.processed = True
            st.session_state.messages = []

            st.success("✅ Documents processed successfully!")

        except Exception as e:
            st.error(f"❌ {e}")
            st.stop()


# Interactive Chat Area
if st.session_state.processed:
    retriever, rag_chain = create_rag_chain(
        st.session_state.collection_name
    )

    # Search Inside Chat History
    search_query = st.text_input(
        "🔍 Search chat history...", 
        placeholder="Type keywords to filter messages"
    )

    for message in st.session_state.messages:
        if search_query and search_query.lower() not in message["content"].lower():
            continue

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and "references" in message:
                st.markdown("---")
                st.markdown("### 📚 References")
                for ref in message["references"]:
                    st.markdown(ref)

    # Suggested Questions Buttons
    st.markdown("##### 💡 Suggested Questions")
    s_col1, s_col2, s_col3 = st.columns(3)

    suggested_clicked = None
    if s_col1.button("📌 Summarize Document", use_container_width=True):
        suggested_clicked = "Summarize the key points of the document."
    elif s_col2.button("🔍 Main Key Concepts", use_container_width=True):
        suggested_clicked = "What are the core concepts covered in this document?"
    elif s_col3.button("❓ Key Takeaways", use_container_width=True):
        suggested_clicked = "List the top 5 takeaways from this text."

    user_input = st.chat_input("Ask a question about your documents...")
    question = user_input or suggested_clicked

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
                reference = f"[{ref_number}] {source} • Page {page + 1}"
            else:
                reference = f"[{ref_number}] {source}"

            references.append(reference)

        assistant_message = {
            "role": "assistant",
            "content": answer,
            "references": references,
        }

        st.session_state.messages.append(assistant_message)

        with st.chat_message("assistant"):
            st.write_stream(stream_text(answer))

            if references:
                st.markdown("---")
                st.markdown("### 📚 References")
                for ref in references:
                    st.markdown(ref)

        st.rerun()

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

### Workflow
1. Select a source.
2. Click **Process Documents**.
3. Ask questions in the chat or use suggested questions.

Happy Learning! 🚀
"""
    )