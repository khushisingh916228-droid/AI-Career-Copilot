from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

pairs = [
    ("ML", "machine learning"),
    ("ML", "cooking"),
    ("data viz", "data visualization"),
    ("JS", "javascript"),
    ("python", "java"),
]

for a, b in pairs:
    emb = model.encode([a, b])
    score = util.cos_sim(emb[0], emb[1]).item()
    print(f"{a!r} vs {b!r}: {score:.2f}")