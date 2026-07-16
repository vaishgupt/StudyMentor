from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

embedding = model.encode("Hello world")

print("Embedding dimension:", len(embedding))
print("Done!")