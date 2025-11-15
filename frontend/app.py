"""
Streamlit frontend for Libya Banks AI.
"""
import streamlit as st
from utils.api_client import api_client
from pathlib import Path
import time

# Page config
st.set_page_config(
    page_title="Libya Banks AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin-top: 1rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

# Header
st.markdown('<div class="main-header">🏦 Libya Banks AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Intelligent Banking Assistant</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📚 Documents")

    # Health check
    with st.expander("🔍 System Status"):
        if st.button("Check Status"):
            health = api_client.health_check()
            if health.get("status") == "healthy":
                st.success("✅ Backend is running")
                st.info(f"LLM Loaded: {health.get('llm_loaded', False)}")
                st.info(f"Documents in DB: {health.get('vector_store_count', 0)}")
            else:
                st.error("❌ Backend is not responding")
                st.error(f"Error: {health.get('error', 'Unknown')}")

    # Document upload
    st.subheader("Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx", "csv"],
        help="Upload banking documents to ask questions about"
    )

    if uploaded_file is not None:
        if st.button("📤 Upload & Process"):
            with st.spinner("Uploading and processing document..."):
                result = api_client.upload_document(uploaded_file)

                if result.get("success"):
                    st.success(f"✅ {result.get('message')}")
                    st.info(f"Chunks created: {result.get('chunks', 0)}")
                else:
                    st.error(f"❌ {result.get('message')}")

    # Process existing documents
    st.subheader("Process Documents")
    if st.button("🔄 Process All Documents"):
        with st.spinner("Processing all documents in data/documents/..."):
            result = api_client.process_all_documents()

            if result.get("success"):
                st.success(f"✅ Processed {result.get('processed', 0)} documents")
                st.info(f"Total chunks: {result.get('total_chunks', 0)}")
            else:
                st.error(f"❌ {result.get('message')}")

    # List documents
    with st.expander("📄 View Documents"):
        docs_result = api_client.list_documents()
        documents = docs_result.get("documents", [])

        if documents:
            for doc in documents:
                st.text(f"📄 {doc['filename']}")
                st.caption(f"Size: {doc['size']} bytes | Type: {doc['type']}")
        else:
            st.info("No documents uploaded yet")

    # Clear conversation
    st.divider()
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    # Example queries
    st.divider()
    st.subheader("💡 Example Queries")
    st.markdown("""
    **📄 Document Q&A:**
    - What are the account opening requirements?
    - What are the wire transfer fees?
    - Explain the overdraft policy

    **💳 Banking Actions:**
    - What is my checking account balance?
    - Show my last 5 transactions
    - Transfer $100 from checking to savings
    - Search for grocery transactions

    **📊 Financial Advisor:**
    - Analyze financial health for customer customer_001
    - What savings plans do you recommend for customer_003?
    - Am I eligible for a home loan? Check customer_001
    - Recommend loans for customer customer_005

    **💬 General:**
    - مرحباً! كيف يمكنك مساعدتي؟ (Arabic support)
    - What can you help me with?
    """)

# Main chat interface
st.divider()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show sources if available
        if message.get("sources"):
            with st.expander("📚 Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**{i}.** {source.get('filename', 'Unknown')}")

# Chat input
if prompt := st.chat_input("Ask me anything about banking..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_data = api_client.chat(prompt, st.session_state.session_id)

            if response_data.get("success"):
                response_text = response_data.get("response", "No response")
                intent = response_data.get("intent", "unknown")
                sources = response_data.get("sources", [])

                # Display response
                st.markdown(response_text)

                # Display sources if available
                if sources:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"**{i}.** {source.get('filename', 'Unknown')} (Chunk {source.get('chunk_index', 0)})")

                # Add to messages
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "sources": sources,
                    "intent": intent
                })
            else:
                error_msg = response_data.get("response", "Error occurred")
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"❌ {error_msg}"
                })

# Footer
st.divider()
st.caption("🏦 Libya Banks AI - Powered by HuggingFace Transformers | Local & Private")