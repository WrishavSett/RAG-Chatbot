import streamlit as st
from rag_utils import extract_text, chunk_text, create_vector_store, search_similar_chunks
from llm_utils import query_ollama

st.set_page_config(layout="centered")

st.title("RAG Chatbot")

# Sidebar controls
with st.sidebar:
    st.markdown("### Options")
    use_context = st.checkbox("Use Document Context", value=True)
    uploaded_files = st.file_uploader(
        "Upload Documents (.pdf, .docx, .txt)", accept_multiple_files=True, type=["pdf", "docx", "txt"]
    )
    if st.button("New Chat"):
        st.session_state["messages"] = []
        st.experimental_rerun()

# Chat section scrollable
chat_container = st.container()
with chat_container:
    st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            margin: auto;
            width: 60%;
        }
        .element-container {
            text-align: justify;
        }
        .stChatMessage {
            overflow-y: auto;
            max-height: 60vh;
        }
    </style>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Load document context if needed
    context_chunks, index = [], None
    if uploaded_files and use_context:
        raw_text = ""
        for file in uploaded_files:
            raw_text += extract_text(file) + "\n"
        chunks = chunk_text(raw_text)
        index, context_chunks = create_vector_store(chunks)

    # Chat loop
    user_query = st.text_input("Ask a question:", key="user_input")
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})

        if use_context:
            if not uploaded_files:
                answer = "Please upload documents to use document context."
            else:
                rel_chunks = search_similar_chunks(user_query, index, context_chunks)
                context = "\n".join(rel_chunks)
                prompt = f"Answer the question based on the following context:\n\n{context}\n\nQuestion: {user_query}"
                answer = query_ollama(prompt)
        else:
            answer = query_ollama(user_query)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    # Display messages
    for msg in st.session_state["messages"]:
        st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")