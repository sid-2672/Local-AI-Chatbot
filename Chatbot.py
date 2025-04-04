import streamlit as st
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
import datetime

# --- Constants ---
DEFAULT_MODEL = "mistral"  
MAX_PDF_SIZE = 10 * 1024 * 1024  # 10MB

# --- Initialize Session State ---
def init_session_state():
    defaults = {
        "doc_text": "",
        "upload_success": False,
        "messages": []  # Store chat history here
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# --- Load CSS ---
def load_css():
    st.markdown("""
    <style>
        .stApp { max-width: 1200px; margin: 0 auto; }
        .chat-message { padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
        .user-message { background-color: #f0f2f6; }
        .ai-message { background-color: #e6f7ff; }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize AI Components ---
def initialize_components():
    try:
        llm = Ollama(model=DEFAULT_MODEL)
        memory = ConversationBufferMemory(memory_key="chat_history", k=5)
        
        prompt = PromptTemplate(
            input_variables=["chat_history", "user_input"],
            template="""You are a helpful AI assistant. Be concise and accurate.
            
            Conversation history:
            {chat_history}
            
            User: {user_input}
            AI:"""
        )
        
        chat_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
        wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=5))
        
        return chat_chain, memory, wiki_tool
    except Exception as e:
        st.error(f"Failed to initialize AI components: {str(e)}")
        st.stop()

# --- Process PDF ---
def process_pdf(uploaded_file):
    try:
        if uploaded_file.size > MAX_PDF_SIZE:
            raise ValueError("File too large. Maximum 10MB allowed.")
        
        reader = PdfReader(uploaded_file)
        text = []
        
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text.append(extracted_text)
        
        full_text = "\n".join(text)
        if not full_text.strip():
            raise ValueError("PDF contains no extractable text.")
        
        return full_text
    except PdfReadError:
        raise ValueError("Invalid PDF file. Please upload a valid PDF.")
    except Exception as e:
        raise ValueError(f"Error processing PDF: {str(e)}")

# --- Save Chat History ---
def save_chat_history():
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"chat_history_{timestamp}.txt"
        
        with open(filename, "w") as f:
            for message in st.session_state.messages:
                role = "User" if message["role"] == "user" else "AI"
                f.write(f"{role}: {message['content']}\n")
        
        return filename
    except Exception as e:
        st.error(f"Failed to save chat history: {str(e)}")
        return None

# --- Main App ---
def main():
    init_session_state()
    load_css()
    chat_chain, memory, wiki_tool = initialize_components()
    
    st.sidebar.header("Settings")
    model_option = st.sidebar.selectbox("AI Model", ["mistral", "llama3", "tinyllama"], index=0)
    
    if model_option != DEFAULT_MODEL:
        with st.spinner(f"Loading {model_option} model..."):
            try:
                chat_chain.llm = Ollama(model=model_option)
                st.rerun()
            except Exception as e:
                st.error(f"Failed to load model: {str(e)}")
    
    st.title("📚 Local AI Chatbot")
    st.caption("Ask questions or upload a PDF for analysis")
    
    # --- PDF Upload ---
    with st.expander("📤 Upload PDF", expanded=not st.session_state.upload_success):
        uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
        if uploaded_file:
            try:
                st.session_state.doc_text = process_pdf(uploaded_file)
                st.session_state.upload_success = True
                st.success(f"✅ PDF processed! ({len(st.session_state.doc_text.split())} words)")
            except Exception as e:
                st.error(str(e))
    
    # --- Chat Display ---
    st.subheader("💬 Chat")
    for message in st.session_state.messages:
        role = "👤 You" if message["role"] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {message['content']}")
    
    # --- User Input ---
    user_input = st.text_area("Your message:", height=100)
    if st.button("Send") and user_input.strip():
        with st.spinner("Thinking..."):
            context = f"Document: {st.session_state.doc_text}\n\n{user_input}" if st.session_state.doc_text else user_input
            response = chat_chain.run(context)
            
            # Fallback to Wikipedia if response is weak
            if len(response.strip()) < 15 or "I don't know" in response.lower():
                wiki_result = wiki_tool.run(user_input)
                if wiki_result:
                    response = f"Wikipedia says:\n\n{wiki_result}"
            
            # Save message to session state
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "ai", "content": response})
            
            st.rerun()
    
    # --- Action Buttons ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("📝 Save Chat"):
            saved_file = save_chat_history()
            if saved_file:
                st.success(f"Chat saved to {saved_file}!")
    
    with col3:
        if st.button("🧹 Clear All"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
# This code is a simple local AI chatbot using Streamlit, Langchain, and Ollama.
# It allows users to upload a PDF, ask questions, and get responses from an AI model.  