import streamlit as st
import logging
from langchain_groq.chat_models import ChatGroq

logging.basicConfig(level=logging.DEBUG)

st.set_page_config(page_title="PioChat", page_icon="🤖")

custom_css = """
<style>
    body {
        font-family: 'Futura', sans-serif;
        background-color: #f5f5f5;
        color: #333333;
    }
    h1 {
        color: #00796b;
        text-align: center;
        margin: 30px 0;
    }
    .stTextInput>div>input {
        background-color: #ffffff;
        color: #333333;
        border: 2px solid #00796b;
        border-radius: 8px;
        padding: 12px;
        font-size: 1.2em;
    }
    .stButton>button {
        background-color: #00796b;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1.2em;
    }
    .stButton>button:hover {
        background-color: #004d40;
    }
    .conversation-history {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 15px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    .social-icons {
        text-align: center;
        margin: 20px 0;
    }
    .social-icons a {
        margin: 0 10px;
        color: #00796b;
        text-decoration: none;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title("PioChat - Your Personal AI Assistant")

st.markdown("""
<div class="social-icons">
    <a href="https://github.com/piodinesh" target="_blank">
        <img src="https://img.icons8.com/ios-filled/50/00796b/github.png" width="30" />
    </a>
    <a href="https://www.linkedin.com/in/pio-dinesh-544984266/" target="_blank">
        <img src="https://img.icons8.com/ios-filled/50/00796b/linkedin.png" width="30" />
    </a>
</div>
""", unsafe_allow_html=True)

api_key = st.text_input("Enter your Groq API Key:", type="password")

if api_key:
    try:
        llm = ChatGroq(model_name="llama-3.1-70b-versatile", api_key=api_key)
        st.success("API Key validated. Start chatting below!")

        if 'conversation' not in st.session_state:
            st.session_state.conversation = []

        query = st.text_input("You:", placeholder="Ask me anything...")
        
        if st.button("Submit"):
            if query:
                response = llm.invoke(query)
                answer = response.content
                
                st.session_state.conversation.append(f"You: {query}")
                st.session_state.conversation.append(f"PioChat: {answer}")

                st.success(f"PioChat: {answer}")
            else:
                st.warning("Please enter a query.")

        if st.session_state.conversation:
            st.write("### Conversation History")
            for message in st.session_state.conversation:
                st.markdown(f"<div class='conversation-history'>{message}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error initializing ChatGroq LLM: {e}")
else:
    st.warning("Please enter your Groq API Key to proceed.")
