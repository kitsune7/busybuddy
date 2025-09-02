from src.busy_buddy.tools import (
  parse_code_snippet,
  parse_qa_pair,
  parse_documentation_response,
)

def sample_code_text() -> str:
  return (
    "TITLE: Basic Usage\n"
    "DESCRIPTION: Show a hello world example.\n\n"
    "SOURCE: https://example.com/hello\n"
    "LANGUAGE: python\n"
    "CODE:\n"
    "```\nprint('hello')\n```\n"
    "----------------------------------------\n"
    "TITLE: Advanced Usage\n"
    "DESCRIPTION: Do something advanced.\n\n"
    "SOURCE: https://example.com/advanced\n"
    "LANGUAGE: javascript\n"
    "CODE:\n"
    "```\nconsole.log('advanced')\n```\n"
  )

def sample_qa_text() -> str:
  return (
    "TOPIC: Installation\n"
    "Q: How do I install it?\n"
    "A: Use your package manager.\n\n"
    "SOURCE: https://example.com/install\n"
    "----------------------------------------\n"
    "TOPIC: Configuration\n"
    "Q: How do I configure it?\n"
    "A: Edit the config file and restart.\n\n"
    "SOURCE: https://example.com/config\n"
  )

def sample_full_doc_text() -> str:
  return (
    "====================\n"
    "CODE SNIPPETS\n"
    "====================\n"
    + sample_code_text()
    + "\n\n"
    "====================\n"
    "Q&A\n"
    "====================\n"
    + sample_qa_text()
  )

def test_parse_code_snippet_extracts_fields():
  text = sample_code_text()
  results = parse_code_snippet(text)

  assert len(results) == 2
  assert results[0]["title"] == "Basic Usage"
  assert results[0]["language"] == "python"
  assert results[0]["code"] == "print('hello')"

  assert results[1]["title"] == "Advanced Usage"
  assert results[1]["language"].lower() in ("javascript", "js")
  assert "console.log" in results[1]["code"]

def test_parse_qa_pair_extracts_fields():
  text = sample_qa_text()
  results = parse_qa_pair(text)

  assert len(results) == 2
  assert results[0]["topic"] == "Installation"
  assert results[0]["question"].startswith("How do I install")
  assert results[0]["answer"].startswith("Use your package manager")
  assert results[0]["source"].startswith("https://")

  assert results[1]["topic"] == "Configuration"
  assert "Edit the config" in results[1]["answer"]

def test_parse_documentation_response_combines_code_and_qa():
  text = sample_full_doc_text()
  result = parse_documentation_response(text)

  assert "snippets" in result and isinstance(result["snippets"], list)
  assert "qa" in result and isinstance(result["qa"], list)
  assert len(result["snippets"]) == 2
  assert len(result["qa"]) == 2
