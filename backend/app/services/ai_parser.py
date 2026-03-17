import os
import requests
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv("backend/.env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def parse_notice(text: str):

    prompt = f"""
Extract deadline information from the following college notice.

Return ONLY valid JSON in this format:
{{
"title": "...",
"date": "...",
"time": "...",
"summary": ["...", "...", "..."]
}}

Do not include explanations or markdown.

Notice:
{text}
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        data = response.json()

        # Debug output
        print("OpenRouter response:", data)

        if "choices" not in data:
            return {
                "title": "API Error",
                "date": "Unknown",
                "time": "Unknown",
                "summary": ["OpenRouter API failed", str(data)]
            }

        result = data["choices"][0]["message"]["content"].strip()

        # SAFETY NET: If the AI forgot the final closing brace, add it for them
        if result.startswith("{") and not result.endswith("}"):
            result += "\n}"

        # IMPROVED PARSING: Find everything between the first '{' and the last '}'
        match = re.search(r'\{.*\}', result, re.DOTALL)
        
        if match:
            cleaned = match.group(0) # Extracts ONLY the JSON dictionary
        else:
            cleaned = result # Fallback if no braces are found

        try:
            parsed = json.loads(cleaned)
            return parsed
        except json.JSONDecodeError as e:
            return {
                "title": "Parsing Failed",
                "date": "Unknown",
                "time": "Unknown",
                "summary": [f"JSON Error: {str(e)}", cleaned]
            }

    except Exception as e:
        return {
            "title": "Server Error",
            "date": "Unknown",
            "time": "Unknown",
            "summary": [str(e)]
        }