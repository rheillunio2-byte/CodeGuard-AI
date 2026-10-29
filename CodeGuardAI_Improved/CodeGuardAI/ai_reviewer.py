import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def review_with_ai_stream(code):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
    if not code.strip():
        raise ValueError("Enter some Python code before requesting a review.")
    if len(code) > 60000:
        raise ValueError("AI review is limited to 60,000 characters per request.")

    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    prompt = f"""You are CodeGuard AI, a careful Python code reviewer.
Review this code for confirmed bugs, security risks, reliability, and readability.
Keep the report concise and prioritize the three most important issues.
For each issue, provide severity, the relevant line or pattern, why it matters, and a practical fix.
Separate confirmed issues from possible concerns. Do not claim you executed the code.
Never repeat any apparent API key, password, token, or other secret; refer to it generically.
Finish with a short overall assessment.

Code to review:
```python
{code}
```"""

    stream = client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config={"max_output_tokens": 1200, "temperature": 0.2},
    )
    for chunk in stream:
        text = getattr(chunk, "text", None)
        if text:
            yield text
