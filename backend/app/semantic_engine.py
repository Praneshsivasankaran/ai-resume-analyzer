from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once (very important)
model = SentenceTransformer('all-MiniLM-L6-v2')


def semantic_similarity_score(resume_text, jd_text):

    # Generate embeddings
    embeddings = model.encode([resume_text, jd_text])

    resume_embedding = embeddings[0].reshape(1, -1)
    jd_embedding = embeddings[1].reshape(1, -1)

    # Compute cosine similarity
    similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]

    score = round(similarity * 100, 2)

    return score, similarity