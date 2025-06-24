"""
convert_to_abaqus.py
Turn plain-English Abaqus requests into runnable Python scripts.
Requires:  langchain, langchain-openai
"""

import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# ------------------------------------------------------------------
# 1)  Initialise the OpenAI chat model
# ------------------------------------------------------------------
#   - Set OPENAI_API_KEY in your shell or a .env file
#   - Use any gpt-4 / gpt-4o / gpt-3.5 model that suits you
llm = ChatOpenAI(
    model_name="gpt-4o-mini",   # or "gpt-4-turbo" | "gpt-4o-latest"
    temperature=0               # deterministic code output
)

# ------------------------------------------------------------------
# 2)  System prompt that instructs the LLM to output ASI-compliant code
# ------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an expert Abaqus/CAE scripting assistant.
• Convert the user’s request into a valid Python script that uses the Abaqus
  Scripting Interface (ASI).
• Always include the two imports:
      from abaqus import *
      from abaqusConstants import *
• The script must be runnable with `abaqus cae noGUI=<script.py>`.
• Use clear variable names and add brief inline comments.
• DO NOT output anything except the code (no prose).  Wrap nothing in Markdown.
"""

# ------------------------------------------------------------------
# 3)  Public helper
# ------------------------------------------------------------------
def generate_abaqus_script(query: str) -> str:
    """
    Convert `query` (plain English) to an Abaqus Python script string.
    """
    messages = [
        SystemMessage(content=SYSTEM_PROMPT.strip()),
        HumanMessage(content=query.strip())
    ]
    response = llm.invoke(messages)
    # Strip backticks if the model adds ```python fences
    text = response.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]  # gets rid of ```python\n
        text = text.rsplit("```", 1)[0]  # removes closing ```
    return text.strip()

# ------------------------------------------------------------------
# 4)  Quick CLI test
# ------------------------------------------------------------------
if __name__ == "__main__":
    example = (
        "Create a 10 mm × 10 mm × 10 mm cube named Cube1, "
        "assign Steel (E=210 GPa, ν=0.3), mesh with 5 mm elements, "
        "and generate a job called CubeJob."
    )
    script = generate_abaqus_script(example)
    print("\n=== Generated Script ===\n")
    print(script)
