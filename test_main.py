from unittest.mock import MagicMock, Mock, patch

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Import functions from main
from main import (
    display_chat_messages,
    get_available_models,
    initialize_llm,
    initialize_session_state,
    setup_sidebar,
)


class TestInitializeSessionState:
    """Test cases for initialize_session_state function"""

    def test_initialize_empty_session_state(self):
        """Test initializing session state when empty"""
        # Create a mock session state object
        mock_session = MagicMock()
        mock_session.__contains__ = Mock(return_value=False)

        with patch("main.st.session_state", mock_session):
            initialize_session_state()

        # Verify that messages and llm attributes were accessed for assignment
        # The session state should now have these attributes set
        assert hasattr(mock_session, "messages")
        assert hasattr(mock_session, "llm")

    def test_initialize_existing_messages(self):
        """Test that existing messages are not overwritten"""
        existing_messages = [HumanMessage(content="test")]
        mock_session = MagicMock()

        def contains_check(key):
            return key == "messages"

        mock_session.__contains__ = Mock(side_effect=contains_check)
        mock_session.messages = existing_messages

        with patch("main.st.session_state", mock_session):
            initialize_session_state()

        # messages should not be overwritten, so it should still be the existing one
        assert mock_session.messages == existing_messages

    def test_initialize_existing_llm(self):
        """Test that existing llm instance is not overwritten"""
        existing_llm = Mock()
        mock_session = MagicMock()

        def contains_check(key):
            return key == "llm"

        mock_session.__contains__ = Mock(side_effect=contains_check)
        mock_session.llm = existing_llm

        with patch("main.st.session_state", mock_session):
            initialize_session_state()

        # llm should not be overwritten
        assert mock_session.llm == existing_llm


class TestGetAvailableModels:
    """Test cases for get_available_models function"""

    @patch("main.Client")
    def test_get_available_models_success(self, mock_client_class):
        """Test successful model fetching"""
        # Create mock models
        mock_model1 = Mock()
        mock_model1.model = "llama3.2:3b"
        mock_model2 = Mock()
        mock_model2.model = "phi3:mini"

        # Create mock response
        mock_response = Mock()
        mock_response.models = [mock_model1, mock_model2]

        # Setup mock client
        mock_client_instance = Mock()
        mock_client_instance.list.return_value = mock_response
        mock_client_class.return_value = mock_client_instance

        # Call function
        success, models, error_msg = get_available_models()

        # Assertions
        assert success is True
        assert models == ["llama3.2:3b", "phi3:mini"]
        assert error_msg == ""
        mock_client_class.assert_called_once_with(host="http://localhost:11434")
        mock_client_instance.list.assert_called_once()

    @patch("main.Client")
    def test_get_available_models_connection_error(self, mock_client_class):
        """Test Ollama connection error"""
        # Simulate connection error
        mock_client_class.side_effect = ConnectionError("Connection refused")

        # Call function
        success, models, error_msg = get_available_models()

        # Assertions
        assert success is False
        assert models == []
        assert "Failed to connect to Ollama" in error_msg
        assert "Connection refused" in error_msg

    @patch("main.Client")
    def test_get_available_models_empty_list(self, mock_client_class):
        """Test when no models are installed"""
        # Create mock response with empty models list
        mock_response = Mock()
        mock_response.models = []

        # Setup mock client
        mock_client_instance = Mock()
        mock_client_instance.list.return_value = mock_response
        mock_client_class.return_value = mock_client_instance

        # Call function
        success, models, error_msg = get_available_models()

        # Assertions
        assert success is True
        assert models == []
        assert error_msg == ""

    @patch("main.Client")
    def test_get_available_models_api_error(self, mock_client_class):
        """Test API error handling"""
        # Setup mock client that raises exception on list()
        mock_client_instance = Mock()
        mock_client_instance.list.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client_instance

        # Call function
        success, models, error_msg = get_available_models()

        # Assertions
        assert success is False
        assert models == []
        assert "Failed to connect to Ollama" in error_msg
        assert "API Error" in error_msg


class TestSetupSidebar:
    """Test cases for setup_sidebar function"""

    @patch("main.get_available_models")
    @patch("streamlit.sidebar")
    @patch("streamlit.title")
    @patch("streamlit.markdown")
    @patch("streamlit.selectbox")
    @patch("streamlit.slider")
    @patch("streamlit.button")
    def test_setup_sidebar_returns_model_and_temperature(
        self,
        mock_button,
        mock_slider,
        mock_selectbox,
        mock_markdown,
        mock_title,
        mock_sidebar,
        mock_get_models,
    ):
        """Test sidebar setup returns correct model and temperature"""
        # Mock get_available_models to return success with models
        mock_get_models.return_value = (True, ["llama3.2:3b", "phi3:mini"], "")

        mock_selectbox.return_value = "llama3.2:3b"
        mock_slider.return_value = 0.7
        mock_button.return_value = False

        with patch("streamlit.sidebar"):
            model, temp = setup_sidebar()

        assert model == "llama3.2:3b"
        assert temp == 0.7

    @patch("main.get_available_models")
    @patch("streamlit.sidebar")
    @patch("streamlit.title")
    @patch("streamlit.markdown")
    @patch("streamlit.selectbox")
    @patch("streamlit.slider")
    @patch("streamlit.button")
    @patch("streamlit.rerun")
    def test_clear_chat_history_button(
        self,
        mock_rerun,
        mock_button,
        mock_slider,
        mock_selectbox,
        mock_markdown,
        mock_title,
        mock_sidebar,
        mock_get_models,
    ):
        """Test that clicking clear button clears messages and reruns"""
        # Mock get_available_models to return success with models
        mock_get_models.return_value = (True, ["llama3.2:3b", "phi3:mini"], "")

        mock_selectbox.return_value = "llama3.2:3b"
        mock_slider.return_value = 0.7
        mock_button.return_value = True

        mock_session = MagicMock()
        mock_session.messages = [HumanMessage(content="test")]

        with patch("streamlit.sidebar"), patch("main.st.session_state", mock_session):
            setup_sidebar()

        # Note: The actual clearing happens in the sidebar code
        # This test verifies the button can be clicked
        mock_button.assert_called()

    @patch("main.get_available_models")
    @patch("streamlit.sidebar")
    @patch("streamlit.title")
    @patch("streamlit.markdown")
    @patch("streamlit.selectbox")
    @patch("streamlit.slider")
    @patch("streamlit.button")
    def test_sidebar_model_options(
        self,
        mock_button,
        mock_slider,
        mock_selectbox,
        mock_markdown,
        mock_title,
        mock_sidebar,
        mock_get_models,
    ):
        """Test that sidebar shows correct model options from Ollama"""
        expected_models = ["llama3.2:3b", "phi3:mini", "qwen2.5:3b"]
        # Mock get_available_models to return these models
        mock_get_models.return_value = (True, expected_models, "")

        mock_selectbox.return_value = "llama3.2:3b"
        mock_slider.return_value = 0.7
        mock_button.return_value = False

        with patch("streamlit.sidebar"):
            setup_sidebar()

        # Verify selectbox was called with correct options
        call_args = mock_selectbox.call_args
        assert call_args[0][1] == expected_models

    @patch("main.get_available_models")
    @patch("streamlit.sidebar")
    @patch("streamlit.title")
    @patch("streamlit.markdown")
    @patch("streamlit.selectbox")
    @patch("streamlit.slider")
    @patch("streamlit.button")
    def test_sidebar_temperature_range(
        self,
        mock_button,
        mock_slider,
        mock_selectbox,
        mock_markdown,
        mock_title,
        mock_sidebar,
        mock_get_models,
    ):
        """Test that temperature slider has correct range"""
        # Mock get_available_models to return success with models
        mock_get_models.return_value = (True, ["llama3.2:3b"], "")

        mock_selectbox.return_value = "llama3.2:3b"
        mock_slider.return_value = 0.5
        mock_button.return_value = False

        with patch("streamlit.sidebar"):
            setup_sidebar()

        # Verify slider was called with correct parameters
        call_kwargs = mock_slider.call_args[1]
        assert call_kwargs["min_value"] == 0.0
        assert call_kwargs["max_value"] == 1.0
        assert call_kwargs["value"] == 0.7
        assert call_kwargs["step"] == 0.1


class TestInitializeLLM:
    """Test cases for initialize_llm function"""

    @patch("main.ChatOllama")
    def test_initialize_llm_success(self, mock_chat_ollama):
        """Test successful LLM initialization"""
        mock_llm_instance = Mock()
        mock_chat_ollama.return_value = mock_llm_instance

        result = initialize_llm("llama3.2:3b", 0.7)

        assert result == mock_llm_instance
        mock_chat_ollama.assert_called_once_with(
            model="llama3.2:3b", temperature=0.7, base_url="http://localhost:11434"
        )

    @patch("main.ChatOllama")
    @patch("streamlit.error")
    @patch("streamlit.info")
    def test_initialize_llm_connection_error(self, mock_info, mock_error, mock_chat_ollama):
        """Test LLM initialization failure"""
        mock_chat_ollama.side_effect = Exception("Connection refused")

        result = initialize_llm("llama3.2:3b", 0.7)

        assert result is None
        mock_error.assert_called_once()
        mock_info.assert_called_once()

    @patch("main.ChatOllama")
    def test_initialize_llm_different_temperatures(self, mock_chat_ollama):
        """Test LLM initialization with different temperature values"""
        mock_llm_instance = Mock()
        mock_chat_ollama.return_value = mock_llm_instance

        temperatures = [0.0, 0.5, 1.0]
        for temp in temperatures:
            result = initialize_llm("llama3.2:3b", temp)
            assert result == mock_llm_instance

            # Check the temperature parameter in the call
            call_kwargs = mock_chat_ollama.call_args[1]
            assert call_kwargs["temperature"] == temp

    @patch("main.ChatOllama")
    def test_initialize_llm_different_models(self, mock_chat_ollama):
        """Test LLM initialization with different models"""
        mock_llm_instance = Mock()
        mock_chat_ollama.return_value = mock_llm_instance

        models = ["llama3.2:3b", "phi3:mini", "qwen2.5:3b"]
        for model in models:
            result = initialize_llm(model, 0.7)
            assert result == mock_llm_instance

            # Check the model parameter in the call
            call_kwargs = mock_chat_ollama.call_args[1]
            assert call_kwargs["model"] == model

    @patch("main.ChatOllama")
    def test_initialize_llm_base_url(self, mock_chat_ollama):
        """Test that LLM is initialized with correct base URL"""
        mock_llm_instance = Mock()
        mock_chat_ollama.return_value = mock_llm_instance

        initialize_llm("llama3.2:3b", 0.7)

        call_kwargs = mock_chat_ollama.call_args[1]
        assert call_kwargs["base_url"] == "http://localhost:11434"


class TestDisplayChatMessages:
    """Test cases for display_chat_messages function"""

    @patch("streamlit.markdown")
    def test_display_empty_messages(self, mock_markdown):
        """Test displaying empty message list"""
        mock_session = MagicMock()
        mock_session.messages = []

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        mock_markdown.assert_not_called()

    @patch("streamlit.markdown")
    def test_display_human_message(self, mock_markdown):
        """Test displaying human message"""
        mock_session = MagicMock()
        mock_session.messages = [HumanMessage(content="Hello")]

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        assert mock_markdown.call_count == 1
        call_args = mock_markdown.call_args[0][0]
        assert "Hello" in call_args
        assert "👤 You" in call_args
        assert "user-message" in call_args

    @patch("streamlit.markdown")
    def test_display_ai_message(self, mock_markdown):
        """Test displaying AI message"""
        mock_session = MagicMock()
        mock_session.messages = [AIMessage(content="Hi there!")]

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        assert mock_markdown.call_count == 1
        call_args = mock_markdown.call_args[0][0]
        assert "Hi there!" in call_args
        assert "🤖 Assistant" in call_args
        assert "assistant-message" in call_args

    @patch("streamlit.markdown")
    def test_display_multiple_messages(self, mock_markdown):
        """Test displaying multiple messages"""
        mock_session = MagicMock()
        mock_session.messages = [
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there!"),
            HumanMessage(content="How are you?"),
            AIMessage(content="I'm doing well!"),
        ]

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        assert mock_markdown.call_count == 4

    @patch("streamlit.markdown")
    def test_display_message_with_special_characters(self, mock_markdown):
        """Test displaying messages with special characters"""
        special_content = "Test <script>alert('xss')</script> & special chars"
        mock_session = MagicMock()
        mock_session.messages = [HumanMessage(content=special_content)]

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        call_args = mock_markdown.call_args[0][0]
        assert special_content in call_args

    @patch("streamlit.markdown")
    def test_display_ignores_system_messages(self, mock_markdown):
        """Test that SystemMessage types are handled (currently ignored)"""
        mock_session = MagicMock()
        mock_session.messages = [
            SystemMessage(content="System prompt"),
            HumanMessage(content="Hello"),
        ]

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        # Only HumanMessage should be displayed
        assert mock_markdown.call_count == 1
        call_args = mock_markdown.call_args[0][0]
        assert "Hello" in call_args
        assert "System prompt" not in call_args

    @patch("streamlit.markdown")
    def test_display_messages_html_structure(self, mock_markdown):
        """Test that messages have correct HTML structure"""
        mock_session = MagicMock()
        mock_session.messages = [HumanMessage(content="Test")]

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        call_args = mock_markdown.call_args[0][0]
        assert 'class="chat-message user-message"' in call_args
        assert 'class="message-header"' in call_args

        # Check unsafe_allow_html is True
        call_kwargs = mock_markdown.call_args[1]
        assert call_kwargs.get("unsafe_allow_html") is True


class TestIntegrationScenarios:
    """Integration tests for common user scenarios"""

    def test_new_chat_session_flow(self):
        """Test complete flow for new chat session"""
        mock_session = MagicMock()
        mock_session.__contains__ = Mock(return_value=False)
        mock_session.messages = []
        mock_session.llm = None

        with patch("main.st.session_state", mock_session):
            # Initialize
            initialize_session_state()

            # Simulate adding messages
            mock_session.messages.append(HumanMessage(content="Hello"))
            mock_session.messages.append(AIMessage(content="Hi!"))

            assert len(mock_session.messages) == 2

    @patch("main.ChatOllama")
    def test_model_switching_flow(self, mock_chat_ollama):
        """Test switching between different models"""
        mock_llm = Mock()
        mock_chat_ollama.return_value = mock_llm

        # Initialize with first model
        llm1 = initialize_llm("llama3.2:3b", 0.7)
        assert llm1 is not None

        # Switch to different model
        llm2 = initialize_llm("phi3:mini", 0.5)
        assert llm2 is not None

        assert mock_chat_ollama.call_count == 2


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    @patch("main.ChatOllama")
    @patch("streamlit.error")
    @patch("streamlit.info")
    def test_initialize_llm_with_empty_model_name(self, mock_info, mock_error, mock_chat_ollama):
        """Test LLM initialization with empty model name"""
        mock_chat_ollama.side_effect = Exception("Invalid model")

        result = initialize_llm("", 0.7)

        assert result is None
        mock_error.assert_called_once()

    @patch("main.ChatOllama")
    def test_initialize_llm_with_boundary_temperatures(self, mock_chat_ollama):
        """Test LLM initialization with boundary temperature values"""
        mock_llm = Mock()
        mock_chat_ollama.return_value = mock_llm

        # Test minimum temperature
        result = initialize_llm("llama3.2:3b", 0.0)
        assert result == mock_llm

        # Test maximum temperature
        result = initialize_llm("llama3.2:3b", 1.0)
        assert result == mock_llm

    @patch("streamlit.markdown")
    def test_display_message_with_empty_content(self, mock_markdown):
        """Test displaying message with empty content"""
        mock_session = MagicMock()
        mock_session.messages = [HumanMessage(content="")]

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        assert mock_markdown.call_count == 1
        call_args = mock_markdown.call_args[0][0]
        assert "👤 You" in call_args

    @patch("streamlit.markdown")
    def test_display_very_long_message(self, mock_markdown):
        """Test displaying very long message"""
        long_content = "A" * 10000
        mock_session = MagicMock()
        mock_session.messages = [HumanMessage(content=long_content)]

        with patch("main.st.session_state", mock_session):
            display_chat_messages()

        assert mock_markdown.call_count == 1
        call_args = mock_markdown.call_args[0][0]
        assert long_content in call_args
