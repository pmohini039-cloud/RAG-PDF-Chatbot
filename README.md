
# 📚 AI Research Assistant

An intelligent **Retrieval-Augmented Generation (RAG)** application that allows users to interact with **PDF documents, Website URLs, and PDF URLs** using natural language. The application retrieves relevant document context using **ChromaDB** and **HuggingFace Embeddings**, then generates accurate responses with **Groq Llama 3.3-70B**.

🔗 **Live Demo:** https://rag-pdf-chatbot-xabxabi7gdrplolz8q4x9m.streamlit.app/

---

## 🚀 Features

- 📄 Upload one or multiple PDF documents
- 🌐 Chat with Website URLs
- 🔗 Chat with PDF URLs
- 💬 Conversational AI with memory
- ⚡ Real-time streaming responses
- 📚 Automatic source references with page numbers
- 📊 Document statistics
- 💡 Suggested follow-up questions
- 📥 Export chat history as TXT
- 📕 Export chat history as PDF
- 🎨 Light/Dark theme support
- ⚡ Powered by Groq Llama 3.3
- 🗂️ ChromaDB Vector Database
- 🤗 HuggingFace Sentence Transformers

---

# 🖼️ Application Screenshots

## 🏠 Home Page

![Home Page](<screenshots/Home%20Page.png>)

---

## 📄 PDF Chat

Upload PDF documents and ask questions about their content.

![PDF Chat](<screenshots/PDF%20Chat.png>)

---

## 🌐 Website Chat

Load website content and interact with it using natural language.

![Website Chat](<screenshots/Website%20Chat.png>)

---

## ✨ Advanced Features

- Document Statistics
- Suggested Questions
- Source References
- Chat Export (TXT & PDF)

![Advanced Features](<screenshots/advanced%20features.png>)

---

# 🏗️ Project Architecture

```
                User
                  │
                  ▼
          Streamlit Interface
                  │
                  ▼
        Document Loader
      (PDF / URL / Website)
                  │
                  ▼
        Text Splitter (Chunks)
                  │
                  ▼
     HuggingFace Embeddings
                  │
                  ▼
          ChromaDB Vector Store
                  │
                  ▼
          Similarity Search
                  │
                  ▼
         Groq Llama 3.3-70B
                  │
                  ▼
       Answer + References
```

---

# 🛠️ Tech Stack

### Frontend

- Streamlit

### LLM

- Groq API
- Llama 3.3 70B Versatile

### RAG Components

- LangChain
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers

### Document Processing

- PyPDF
- BeautifulSoup4

### Export

- ReportLab

---

# 📂 Project Structure

```
RAG-PDF-Chatbot/
│
├── app.py
├── config.py
├── rag/
│   ├── rag_chain.py
│   └── memory.py
│
├── utils/
│   ├── pdf_loader.py
│   ├── website_loader.py
│   ├── pdf_downloader.py
│   ├── chunker.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── streamer.py
│   └── chat_export.py
│
├── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/pmohini039-cloud/RAG-PDF-Chatbot.git

cd RAG-PDF-Chatbot
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---

# 💡 Example Questions

### PDF

- Summarize the document.
- Explain the key concepts.
- Give examples from the document.
- What are the important topics?

### Website

- Summarize the webpage.
- Explain this tutorial.
- What are the key takeaways?

### PDF URL

- Explain the uploaded PDF.
- List the important concepts.
- Generate concise notes.

---

# 🎯 Future Improvements

- Multi-document comparison
- OCR support for scanned PDFs
- Voice input
- Citation highlighting
- Hybrid Search (BM25 + Vector Search)
- Multi-language support
- User authentication

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Mohini Patil**

GitHub: https://github.com/pmohini039-cloud

---

⭐ If you found this project useful, consider giving it a star on GitHub!
