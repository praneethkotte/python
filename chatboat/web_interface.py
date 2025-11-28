import streamlit as st
from agents import AIAgentSystem


def run_web_interface():
    st.set_page_config(page_title="AI Agent System", page_icon="🤖")
    st.title("🚀 AI Agent System")
    st.sidebar.title("🛠️ Agents Available")
    st.sidebar.markdown(
        """
    - 🤖 **Code Agent** (Python, JS, etc.)
    - 🔢 **Math Agent** (Calculations)
    - 📰 **News Agent** (Current events)
    - 🔍 **Search Agent** (Web search)
    """
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    ai_system = AIAgentSystem()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ai_system.process_query(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
