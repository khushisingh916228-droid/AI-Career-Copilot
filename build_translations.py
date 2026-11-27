import ast
import json
import os
import re
import sys
import time

sys.path.insert(0, "mock_interview_bot")
from llm_client import ask_llm

LANGS = {"hi": "Hindi (Devanagari script)", "pa": "Punjabi (Gurmukhi script)"}
OUT = "translations.json"
BATCH = 20

with open("app.py", encoding="utf-8") as f:
    tree = ast.parse(f.read())

strings = set()
for node in ast.walk(tree):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "tr" and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)):
        strings.add(node.args[0].value)
strings = sorted(strings)
print("fixed strings found:", len(strings))

data = {}
if os.path.exists(OUT):
    try:
        with open(OUT, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}


def save():
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def translate_batch(batch, lang_name):
    prompt = (
        "Translate each UI text below from English into " + lang_name + ". "
        "Keep emojis, numbers, brand names and technical terms (AI, ATS, PDF, SQL, Gemini) in English where natural. "
        "Return ONLY a JSON array of strings, with the same length and order as the input, and no explanation.\n\n"
        + json.dumps(batch, ensure_ascii=False)
    )
    raw = ask_llm(prompt, temperature=0.2)
    m = re.search(r"\[.*\]", raw, re.S)
    arr = json.loads(m.group(0))
    if not isinstance(arr, list) or len(arr) != len(batch):
        raise ValueError("length mismatch")
    return [str(x) for x in arr]


for lang, lang_name in LANGS.items():
    done = data.setdefault(lang, {})
    todo = [s for s in strings if s not in done]
    print(lang, "to translate:", len(todo))
    failed = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        ok = False
        for attempt in range(3):
            try:
                out = translate_batch(batch, lang_name)
                for s, tr_text in zip(batch, out):
                    done[s] = tr_text
                ok = True
                break
            except Exception as e:
                print("retry", lang, i, type(e).__name__)
                time.sleep(5)
        if not ok:
            failed += len(batch)
        save()
        print(lang, min(i + BATCH, len(todo)), "/", len(todo))
        time.sleep(2)
    print(lang, "failed:", failed)

print("finished")
