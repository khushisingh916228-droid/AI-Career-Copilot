import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

GROQ_MODEL = "openai/gpt-oss-120b"
GEMINI_MODEL = "gemini-3.6-flash"  # model used as the Gemini fallback


def _ask_groq(prompt, system, temperature):
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY missing")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={"model": GROQ_MODEL, "messages": messages, "temperature": temperature},
        timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Groq status {r.status_code}")
    return r.json()["choices"][0]["message"]["content"].strip()


def _ask_gemini(prompt, system, temperature):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")

    import google.generativeai as genai
    genai.configure(api_key=key)
    model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=system or None)
    response = model.generate_content(
        prompt, generation_config={"temperature": temperature}
    )
    return response.text.strip()


# Try Groq first; if it fails (limit/error), fall back to Gemini
PROVIDERS = [("groq", _ask_groq), ("gemini", _ask_gemini)]


def ask_llm(prompt, system=None, temperature=0.7):
    """Tries each provider in order. Raises RuntimeError if all of them fail."""
    errors = []
    for name, fn in PROVIDERS:
        try:
            text = fn(prompt, system, temperature)
            if text:
                print(f"[llm] answered by {name}")
                return text
        except Exception as e:
            errors.append(f"{name}: {type(e).__name__} {str(e)[:80]}")
    raise RuntimeError("All AI providers failed -> " + " | ".join(errors))