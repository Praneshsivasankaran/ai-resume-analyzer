from sentence_transformers import SentenceTransformer, util

# Load model once when server starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def keyword_match_score(resume_text, jd_text):

    # Generate embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)

    # Calculate semantic similarity
    similarity_score = util.cos_sim(resume_embedding, jd_embedding).item()

    # Convert to percentage score
    keyword_score = int(similarity_score * 100)

    # Simple missing keyword detection
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    missing_keywords = list(jd_words - resume_words)

    return keyword_score, similarity_score, missing_keywords[:10]