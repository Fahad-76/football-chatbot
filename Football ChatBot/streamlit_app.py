import streamlit as st
from app.chatbot import handle_query  # ✅ Assuming handle_query is defined in app/chatbot/__init__.py or a .py file inside

st.title("⚽ Football ChatBot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Ask a football question (e.g., 'top scorer'): ")

# If there's input, process it
if user_input:
    try:
        response = handle_query(user_input)  # 👈 Call your chatbot logic
    except Exception as e:
        response = f"Error: {e}"

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")


