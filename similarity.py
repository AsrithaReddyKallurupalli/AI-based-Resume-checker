from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(embedding1, embedding2):
    # Ensure inputs are 2D arrays (1, embedding_dim)
    # Cosine similarity returns a matrix (1x1 in this case)
    return cosine_similarity(embedding1, embedding2)[0][0]
