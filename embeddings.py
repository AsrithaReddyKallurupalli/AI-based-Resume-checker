from sentence_transformers import SentenceTransformer

# Load model globally to avoid reloading often
# 'all-MiniLM-L6-v2' is a good balance of speed and accuracy
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text):
    if isinstance(text, str):
        text = [text]
    return model.encode(text)
