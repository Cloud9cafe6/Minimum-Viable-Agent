import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Smart Researcher Agent", layout="wide")
st.title("🤖 Smart Researcher Agent")
st.caption("Powered by Gemini AI & Live Web Search")

# Sidebar for API Key (So you don't hardcode it in GitHub)
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")

if not api_key:
    st.warning("Please enter your API Key in the sidebar to start.")
    st.stop()

# Configure the Model (Layer 4: Models)
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 2. THE TOOL (Layer 5: Tools & Actions) ---
def search_web(query):
    """Searches the web and returns top results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Search failed: {e}"

# --- 3. THE AGENT LOGIC (Layer 2: Planning) ---
def run_agent(user_query):
    with st.spinner("🔍 Searching the web..."):
        search_results = search_web(user_query)
    
    with st.spinner("🧠 Thinking and summarizing..."):
        prompt = f"""
        You are an expert research assistant. 
        Based on the following search results, answer the user's question clearly and concisely.
        Include bullet points and cite the sources.
        
        USER QUESTION: {user_query}
        
        SEARCH RESULTS:
        {search_results}
        """
        response = model.generate_content(prompt)
        return response.text, search_results

# --- 4. THE INTERFACE (Layer 1: Interface) ---
user_query = st.text_input("What do you want to research today?", placeholder="e.g., Latest news on AI agents")

if st.button("Research") and user_query:
    if not api_key:
        st.error("API Key is missing!")
    else:
        # Run the agent
        final_answer, raw_data = run_agent(user_query)
        
        # Display results
        st.subheader("📝 Research Report")
        st.write(final_answer)
        
        with st.expander("View Raw Search Data"):
            st.text(raw_data)
