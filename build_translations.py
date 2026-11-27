import ast
import json
import os
import sys
import time

sys.path.insert(0, "multilingual_layer")
import main as ml

LANGS = ["hi", "pa"]
OUT = "translations.json"

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
    with open(OUT, encoding="utf-8") as f:
        data = json.load(f)


def save():
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


for lang in LANGS:
    done = data.setdefault(lang, {})
    todo = [s for s in strings if s not in done]
    print(lang, "to translate:", len(todo))
    failed = 0
    for i, s in enumerate(todo, 1):
        try:
            done[s] = ml.translate_text(s, lang, max_retries=3, raise_on_fail=True)
        except Exception:
            failed += 1
            time.sleep(5)
        if i % 20 == 0:
            save()
            print(lang, i, "/", len(todo))
    save()
    print(lang, "failed:", failed)

print("finished")
