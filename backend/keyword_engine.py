from functools import lru_cache
from sentence_transformers import SentenceTransformer, util

# Load model once when server starts
model = SentenceTransformer("all-MiniLM-L6-v2")


# Cache embeddings to avoid recomputing
@lru_cache(maxsize=128)
def get_embedding(text):
    return model.encode(text, convert_to_tensor=True)


def keyword_match_score(resume_text, jd_text):

    # Get cached embeddings
    resume_embedding = get_embedding(resume_text)
    jd_embedding = get_embedding(jd_text)

    # Calculate semantic similarity
    similarity_score = util.cos_sim(resume_embedding, jd_embedding).item()

    # Convert similarity to percentage
    keyword_score = int(similarity_score * 100)

    # Detect missing keywords
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    missing_keywords = list(jd_words - resume_words)

    return keyword_score, similarity_score, missing_keywords[:10]