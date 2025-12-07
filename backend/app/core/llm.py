import json
import re
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_json(text: str):
    match = re.search(r"\[\s*{.*}\s*\]", text, re.DOTALL)
    if match:
        return match.group(0)
    return None

def generate_task_plan(goal: str):
    prompt = f"""
    You are an expert project planner.

    Break the following goal into detailed practical tasks. 
    Descriptions must be specific, actionable, and explain the purpose + expected outcome.
    Avoid generic content.

    Return ONLY a valid JSON array of objects like:

    [
    {{
        "id": "T1",
        "name": "Precise task title",
        "description": "Explains what must be done, how to do it, and what output is expected",
        "depends_on": [],
        "estimated_days": 3
    }}
    ]

    Goal: "{goal}"
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content.strip()

    json_str = extract_json(output)

    if not json_str:
        print("JSON parse error:", output)
        return []

    return json.loads(json_str)
