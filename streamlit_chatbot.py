#!/usr/bin/env python3
"""Streamlit-based web UI chatbot."""

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from ollama import Client


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "llm" not in st.session_state:
        st.session_state.llm = None


def get_available_models():
    """Fetch available models from local Ollama instance

    Returns:
        tuple: (success: bool, models: List[str], error_message: str)
    """
    try:
        client = Client(host="http://localhost:11434")
        response = client.list()
        model_names = [model.model for model in response.models]
        return (True, model_names, "")
    except Exception as e:
        error_msg = f"Failed to connect to Ollama: {e!s}"
        return (False, [], error_msg)


def setup_page():
    st.set_page_config(
        page_title="LLM Chatbot",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .main {
            background-color: #0e1117;
        }
        .stTextInput > div > div > input {
            background-color: #1e1e1e;
            color: white;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .user-message {
            background-color: #1e3a5f;
            border-left: 4px solid #4a9eff;
        }
        .assistant-message {
            background-color: #1e2d1e;
            border-left: 4px solid #4ade80;
        }
        .message-header {
            font-weight: bold;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }
        .stButton > button {
            background-color: #4a9eff;
            color: white;
            border-radius: 0.5rem;
            border: none;
            padding: 0.5rem 2rem;
            font-weight: 600;
        }
        .stButton > button:hover {
            background-color: #3b7fd9;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def setup_sidebar():
    """Configure sidebar with model settings"""

    with st.sidebar:
        st.title("⚙️ Settings")

        st.markdown("### Model Configuration")

        # Fetch available models from Ollama
        success, model_options, error_msg = get_available_models()

        # Handle different scenarios
        if not success:
            # Ollama is not running - show error
            st.error(error_msg)
            st.info("Make sure Ollama is running. Start it with: `ollama serve`")
            model_options = []  # Empty list
        elif len(model_options) == 0:
            # Ollama is running but no models installed
            st.warning("No models found in Ollama.")
            st.info("Install a model using: `ollama pull llama3.2:3b`")

        # Only show selectbox if models are available
        if len(model_options) > 0:
            selected_model = st.selectbox(
                "Select Model",
                model_options,
                help="Choose from your installed Ollama models",
            )
        else:
            selected_model = None  # No model selected
            st.info("👆 Install a model first to start chatting")

        temperature = st.slider(
            "Createtivity (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make output more creative",
        )

        st.markdown("---")

        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This chatbot uses **Ollama** for local LLM inference.

        **Features:**
        - 🚀 Fast local inference
        - 🔒 Privacy-focused
        - 💡 Lightweight models
        - 🎨 Clean UI
        """)

        return selected_model, temperature


def initialize_llm(model_name, temperature):
    """Initialize or update the LLM instance"""
    try:
        llm = ChatOllama(
            model=model_name, temperature=temperature, base_url="http://localhost:11434"
        )
        return llm
    except Exception as e:
        st.error(f"Failed to connect to Ollama: {e!s}")
        st.info("Make sure Ollama is running. Start it with: `ollama serve`")
        return None


def display_chat_messages(stream=False):
    """Display all chat messages"""
    if stream:
        st.markdown(
            f"""
                <div class="chat-message assistant-message">
                    <div class="message-header">🤖 Assistant</div>
                    <div>{st.session_state.messages[-1].content}</div>
                </div>
            """,
            unsafe_allow_html=True,
        )
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            st.markdown(
                f"""
                <div class="chat-message user-message">
                    <div class="message-header">👤 You</div>
                    <div>{message.content}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        elif isinstance(message, AIMessage):
            st.markdown(
                f"""
                <div class="chat-message assistant-message">
                    <div class="message-header">🤖 Assistant</div>
                    <div>{message.content}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )


def main():
    setup_page()
    initialize_session_state()

    selected_model, temperature = setup_sidebar()

    st.title("🤖 Chatbot")
    st.markdown("Chat with a local LLM using Ollama")

    # Check if a model was selected
    if selected_model is None:
        st.warning("⚠️ No model available. Please install Ollama models to continue.")
        st.code("ollama pull llama3.2:3b", language="bash")
        return

    llm = initialize_llm(selected_model, temperature)

    if llm is None:
        st.warning("⚠️ Please ensure Ollama is running and the selected model is installed.")
        st.code(f"ollama pull {selected_model}", language="bash")
        return

    st.session_state.llm = llm

    display_chat_messages()

    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))

        with st.spinner("🤔 Thinking..."):
            try:
                print("Invoking LLM...")
                response = st.session_state.llm.stream([HumanMessage(content=user_input)])
                for chunk in response:
                    if chunk.text:
                        if len(st.session_state.messages) == 0 or not isinstance(
                            st.session_state.messages[-1], AIMessage
                        ):
                            st.session_state.messages.append(AIMessage(content=chunk.text))
                        else:
                            st.session_state.messages[-1].content += chunk.text
                        display_chat_messages(stream=True)
                st.session_state.messages.append(AIMessage(content=response.content))
            except Exception as e:
                print(e, "here")
                st.session_state.error = f"Error generating response: {e!s}"
                st.info("Please check if the model is downloaded and Ollama is running.")

        st.rerun()


if __name__ == "__main__":
    main()
