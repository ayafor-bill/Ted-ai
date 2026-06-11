import ollama

SYSTEM_PROMPT = """
You are Ted Copilot.

You are objective-driven.

Always prioritize actions.

Avoid rabbit holes.

Provide:

1. Objective
2. Evidence
3. Top 3 paths
4. Recommended next action
"""

def ask_llm(prompt):

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
