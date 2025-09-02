from unittest.mock import patch, MagicMock

def test_main_invokes_agent_with_user_input(monkeypatch):
  user_prompt = "Find React router docs"
  monkeypatch.setattr("builtins.input", lambda *_: user_prompt)

  class DummyModel:
    def __init__(self, *_, **kwargs):
      self.kwargs = kwargs

  agent_instance = MagicMock()

  with patch("src.busy_buddy.main.OpenAIServerModel", DummyModel), \
      patch("src.busy_buddy.main.ToolCallingAgent", return_value=agent_instance):
    from src.busy_buddy.main import run_application

    run_application()

    assert agent_instance.run.call_count == 1
    _, kwargs = agent_instance.run.call_args
    assert "additional_args" in kwargs
    assert kwargs["additional_args"].get("user_prompt") == user_prompt
