from smolagents import (
  ToolCallingAgent,
  OpenAIServerModel
)

import dotenv
import os

from .tools import fetch_library_docs

def run_application():
  dotenv.load_dotenv()

  max_steps = 5
  tools = [fetch_library_docs]
  model = OpenAIServerModel(
    model_id="gemini-2.5-flash",
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
  )

  agent = ToolCallingAgent(
    max_steps=max_steps,
    tools=tools,
    model=model,
  )

  user_input = input("What kind of documentation can I look up for you?\n> ")
  agent.run("Fetch code documentation the user is looking for. If you can't find any documentation with the `fetch_library_docs` tool, rely on your internal knowledge as a last resort. After fetching the documentation, respond to the user with a code example, a brief explanation, and a list of one or more sources used to create the code example. Do not list sources if only internal knowledge was used.", additional_args={"user_prompt": user_input})

if __name__ == "__main__":
  run_application()
