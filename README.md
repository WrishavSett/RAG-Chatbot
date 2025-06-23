# RAG Chatbot with Streamlit and Ollama

This is a Retrieval-Augmented Generation (RAG) chatbot built using Streamlit and locally hosted models via [Ollama](https://ollama.com/). The app allows users to upload documents and ask questions that are answered using both the document context and language model reasoning.

## Features

- Document upload support: `.pdf`, `.docx`, `.txt`
- Local embedding generation and similarity search using FAISS
- Context-aware or plain query mode
- Streamlit web interface
- Uses Ollama for both embeddings and LLM responses

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── llm_utils.py        # Interfacing with Ollama LLM API for text generation
├── rag_utils.py        # Utilities for document parsing, chunking, embedding, and similarity search
└── README.md           # Project documentation
```

### `app.py`
- Initializes Streamlit app layout and session state
- Handles document uploads via sidebar
- Switch between context-aware or standalone chat
- Displays the chat history

### `llm_utils.py`
- Provides a function `query_ollama` to interact with the Ollama local language model API

### `rag_utils.py`
- Functions for parsing `.pdf`, `.docx`, and `.txt` files
- Token-based chunking using `tiktoken`
- Embedding generation using Ollama embedding model (`nomic-embed-text`)
- Vector store creation and similarity search using FAISS

## Requirements

- Python 3.8+
- Ollama running locally with models:
  - `llama3.2:3b` for text generation
  - `nomic-embed-text` for embeddings
- Python packages:
  - `streamlit`
  - `requests`
  - `faiss-cpu`
  - `numpy`
  - `tiktoken`
  - `PyPDF2`
  - `python-docx`

## Running the App

1. Start the Ollama server with required models.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the app:
    ```bash
    streamlit run app.py
    ```

## Notes

- Ensure the Ollama API is accessible at `http://localhost:11434`
- You can reset the chat using the **New Chat** button in the sidebar