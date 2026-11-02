import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Smart Researcher Agent", layout="wide")
st.title("🤖 Smart Researcher Agent (With Memory)")
st.caption("Remembers our conversation and searches the live web!")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")

if not api_key:
    st.warning("Please enter your API Key in the sidebar to start.")
    st.stop()

# Configure the Model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.8-flash')

# --- 2. MEMORY INITIALIZATION (Layer 3) ---
# Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Gemini's built-in chat session to remember context
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- 3. THE TOOL (Layer 5: Tools & Actions) ---
def search_web(query):
    """Searches the web and returns top results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Search failed: {e}"

# --- 4. DISPLAY CHAT HISTORY ---
# Render all previous messages from memory
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. THE AGENT LOGIC & INTERFACE (Layer 1 & 2) ---
if prompt := st.chat_input("What do you want to research or ask?"):
    # A. Add user message to memory and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # B. Agent searches the live web for the latest query
    with st.spinner("🔍 Searching the live web..."):
        search_results = search_web(prompt)
    
    # C. Build an augmented prompt that includes both the search results AND conversational context
    augmented_prompt = f"""
    You are an expert research assistant. You have memory of our ongoing conversation.
    Based on the following live search results, answer the user's question clearly.
    If this is a follow-up question, use the search results to inform your answer while maintaining the conversational context.
    
    LIVE SEARCH RESULTS:
    {search_results}
    
    USER QUESTION: {prompt}
    """

    # D. Get response from the chat session (which automatically tracks history)
    with st.spinner("🧠 Thinking and summarizing..."):
        try:
            response = st.session_state.chat.send_message(augmented_prompt)
            response_text = response.text
            
            # E. Add assistant response to memory and display it
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"):
                st.markdown(response_text)
                
        except Exception as e:
            st.error(f"Error generating response: {e}")
