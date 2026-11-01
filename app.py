import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Smart Researcher Agent", layout="centered")
st.title("🤖 Smart Researcher Agent")
st.markdown("Powered by Gemini 3.8 Flash, Live Web Search, & Persistent Memory")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")

if not api_key:
    st.warning("👈 Please enter your Google Gemini API Key in the sidebar to start.")
    st.stop()

# Configure the Model with Gemini 3.8 Flash
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.8-flash')

# Initialize chat history in Streamlit session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. THE TOOL ---
def search_web(query):
    """Searches the web and returns top results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Search failed: {e}"

# --- 3. DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. THE AGENT & CHAT INPUT ---
if user_query := st.chat_input("What do you want to research or discuss?"):
    # Append user message to state and display it
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Run agent logic with search and chat history context
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching live web & reviewing conversation history..."):
            # Perform search based on latest query
            search_results = search_web(user_query)
            
            # Format past conversation history into the prompt
            history_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[:-1]])
            
            prompt = f"""
            You are an expert research assistant powered by Gemini 3.8 Flash with access to ongoing conversation history.
            
            CONVERSATION HISTORY:
            {history_text}
            
            NEW USER QUESTION: {user_query}
            
            LIVE SEARCH RESULTS:
            {search_results}
            
            Instructions: Answer the user's new question clearly, building upon the context of the conversation history when relevant. Include bullet points and citations.
            """
            
            response = model.generate_content(prompt)
            final_answer = response.text
            
            st.markdown(final_answer)
            
            # Save assistant response to state
            st.session_state.messages.append({"role": "assistant", "content": final_answer})import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Smart Researcher Agent", layout="centered")
st.title("🤖 Smart Researcher Agent")
st.markdown("Powered by Gemini 3.8 Flash, Live Web Search, & Persistent Memory")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")

if not api_key:
    st.warning("👈 Please enter your Google Gemini API Key in the sidebar to start.")
    st.stop()

# Configure the Model with Gemini 3.8 Flash
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.8-flash')

# Initialize chat history in Streamlit session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. THE TOOL ---
def search_web(query):
    """Searches the web and returns top results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Search failed: {e}"

# --- 3. DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. THE AGENT & CHAT INPUT ---
if user_query := st.chat_input("What do you want to research or discuss?"):
    # Append user message to state and display it
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Run agent logic with search and chat history context
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching live web & reviewing conversation history..."):
            # Perform search based on latest query
            search_results = search_web(user_query)
            
            # Format past conversation history into the prompt
            history_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[:-1]])
            
            prompt = f"""
            You are an expert research assistant powered by Gemini 3.8 Flash with access to ongoing conversation history.
            
            CONVERSATION HISTORY:
            {history_text}
            
            NEW USER QUESTION: {user_query}
            
            LIVE SEARCH RESULTS:
            {search_results}
            
            Instructions: Answer the user's new question clearly, building upon the context of the conversation history when relevant. Include bullet points and citations.
            """
            
            response = model.generate_content(prompt)
            final_answer = response.text
            
            st.markdown(final_answer)
            
            # Save assistant response to state
            st.session_state.messages.append({"role": "assistant", "content": final_answer})
