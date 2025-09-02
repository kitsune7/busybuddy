from unittest.mock import patch

from src.busy_buddy.tools import fetch_library_docs

class FakeResponse:
  def __init__(self, status_code=200, text="", json_obj=None):
    self.status_code = status_code
    self.text = text
    self._json = json_obj

  def json(self):
    if self._json is None:
      raise ValueError("No json set")
    return self._json

def mocked_requests_get_success(url, *args, **kwargs):
  if url.startswith("https://context7.com/api/v1/search"):
    payload = {"results": [{"id": "/vercel/next.js"}]}
    return FakeResponse(status_code=200, json_obj=payload)
  if url.startswith("https://context7.com/api/v1/vercel/next.js"):
    text = (
      "====================\nCODE SNIPPETS\n====================\n"
      "TITLE: Example\nDESCRIPTION: Demo\n\nSOURCE: https://docs\nLANGUAGE: python\n"
      "CODE:\n```\nprint('ok')\n```\n"
    )
    return FakeResponse(status_code=200, text=text)
  return FakeResponse(status_code=404, text="Not Found")

def mocked_requests_get_search_no_results(url, *args, **kwargs):
  if url.startswith("https://context7.com/api/v1/search"):
    payload = {"results": []}
    return FakeResponse(status_code=200, json_obj=payload)
  return FakeResponse(status_code=404)

def mocked_requests_get_docs_error(url, *args, **kwargs):
  if url.startswith("https://context7.com/api/v1/search"):
    payload = {"results": [{"id": "/org/pkg"}]}
    return FakeResponse(status_code=200, json_obj=payload)
  if url.startswith("https://context7.com/api/v1/org/pkg"):
    return FakeResponse(status_code=500, text="oops")
  return FakeResponse(status_code=404)

@patch("src.busy_buddy.tools.requests.get", side_effect=mocked_requests_get_success)
def test_fetch_library_docs_success(*args, **kwargs):
  result = fetch_library_docs(query="next.js", topic="routing")
  assert isinstance(result, dict)
  assert "snippets" in result and isinstance(result["snippets"], list)
  assert len(result["snippets"]) == 1
  assert result["snippets"][0]["code"] == "print('ok')"

@patch("src.busy_buddy.tools.requests.get", side_effect=mocked_requests_get_search_no_results)
def test_fetch_library_docs_no_results(*args, **kwargs):
  result = fetch_library_docs(query="missing-lib", topic="anything")
  assert isinstance(result, str)
  assert "No documentation found" in result

@patch("src.busy_buddy.tools.requests.get", side_effect=mocked_requests_get_docs_error)
def test_fetch_library_docs_docs_error(*args, **kwargs):
  result = fetch_library_docs(query="org-pkg", topic="intro")
  assert isinstance(result, str)
  assert "Error fetching documentation" in result or "Received status code" in result
