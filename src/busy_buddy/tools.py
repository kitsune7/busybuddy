from smolagents import tool
from typing import TypedDict
import requests
import json
import re

QA = TypedDict("QA", {
  "topic": str,
  "question": str,
  "answer": str,
  "source": str
})
CodeSnippet = TypedDict("CodeSnippet", {
  "title": str,
  "description": str,
  "source": str,
  "language": str,
  "code": str
})
DocumentationResult = TypedDict("DocumentationResult", {
  "snippets": list[CodeSnippet],
  "qa": list[QA]
})

@tool
def fetch_library_docs(query: str, topic: str) -> DocumentationResult:
    """
    This is a tool that fetches documentation for a specific code library, framework, or API.

    Args:
      query: The name of the library, framework, or API to fetch documentation for.
      topic: The specific topic within the library or framework to fetch documentation for.
    """

    library_search_api_url = f"https://context7.com/api/v1/search?query={query}"
    library_id = None

    response = requests.get(library_search_api_url)
    if response.status_code == 200:
      data = response.json()
      results = data.get("results", [])
      if len(results) == 0:
        raise Exception(f"No documentation found for '{query}'.")
      elif not results[0].get("id", ""):
        raise Exception(f"Couldn't find library ID for\n'{json.dumps(results[0], indent=2)}'.")
      else:
        library_id = results[0]['id']

    documentation_api_url = f"https://context7.com/api/v1{library_id}?topic={topic}"

    response = requests.get(documentation_api_url)
    if response.status_code == 200:
      return parse_documentation_response(response.text)
    else:
      raise Exception(f"Error fetching documentation for {library_id} with topic \"{topic}\": {response.status_code} - {response.text}")

def parse_documentation_response(text: str) -> DocumentationResult:
  result: DocumentationResult = {
    "snippets": [],
    "qa": []
  }
  header_pattern = r'={4,}\n.+\n={4,}'
  groups = re.split(header_pattern, text.strip())

  for group in groups:
    if "CODE:" in group:
      result["snippets"] = parse_code_snippet(group)
    elif "Q:" in group and "A:" in group:
      result["qa"] = parse_qa_pair(group)

  return result

def parse_code_snippet(text: str) -> list[CodeSnippet]:
  results = []
  separator = '----------------------------------------'

  lines = text.strip().split('\n')
  sections = '\n'.join(lines).split(separator)
  for section in sections:
    section = section.strip()
    code_snippet = {}

    # re.MULTILINE is needed because each section contains more than one line and we're searching it all simultaneously
    title_match = re.match(r'^TITLE:\s*(.*)$', section, re.MULTILINE)
    description_match = re.search(r'^DESCRIPTION:\s*(.*)$', section, re.MULTILINE)
    source_match = re.search(r'^SOURCE:\s*(.*)$', section, re.MULTILINE)
    language_match = re.search(r'^LANGUAGE:\s*(.*)$', section, re.MULTILINE)
    code_match = re.search(r'^CODE:\s*\n```(?:\w+)?\n(.*)\n```', section, re.MULTILINE | re.DOTALL)

    code_snippet["title"] = title_match.group(1).strip() if title_match else ""
    code_snippet["description"] = description_match.group(1).strip() if description_match else ""
    code_snippet["source"] = source_match.group(1).strip() if source_match else ""
    code_snippet["language"] = language_match.group(1).strip() if language_match else ""
    code_snippet["code"] = code_match.group(1).strip() if code_match else ""

    results.append(code_snippet)

  return results

def parse_qa_pair(text: str) -> list[QA]:
  results = []
  separator = '----------------------------------------'

  lines = text.strip().split('\n')
  sections = '\n'.join(lines).split(separator)
  for section in sections:
    section = section.strip()
    qa_pair = {}

    # re.MULTILINE is needed because each section contains more than one line and we're searching it all simultaneously
    topic_match = re.match(r'^TOPIC:\s*(.*)$', section, re.MULTILINE)
    question_match = re.search(r'^Q:\s*(.*)$', section, re.MULTILINE)
    answer_match = re.search(r'^A:\s*(.*)\n\n', section, re.MULTILINE | re.DOTALL)
    source_match = re.search(r'^SOURCE:\s*(.*)$', section, re.MULTILINE)

    qa_pair["topic"] = topic_match.group(1).strip() if topic_match else ""
    qa_pair["question"] = question_match.group(1).strip() if question_match else ""
    qa_pair["answer"] = answer_match.group(1).strip() if answer_match else ""
    qa_pair["source"] = source_match.group(1).strip() if source_match else ""

    results.append(qa_pair)

  return results
