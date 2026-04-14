from functools import lru_cache
from sentence_transformers import SentenceTransformer, util
import re

# Load model once at import time
model = SentenceTransformer("all-MiniLM-L6-v2")

# Common English stop-words we never want to surface as "missing keywords"
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "for", "nor", "on", "at", "to",
    "from", "by", "of", "in", "with", "as", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "should", "could", "may", "might", "must", "can",
    "this", "that", "these", "those", "i", "you", "he", "she", "it",
    "we", "they", "them", "their", "our", "your", "its", "if", "then",
    "than", "so", "not", "no", "yes", "all", "any", "some", "each",
    "every", "more", "most", "other", "such", "only", "own", "same",
    "about", "into", "through", "during", "before", "after", "above",
    "below", "up", "down", "out", "off", "over", "under", "again",
    "further", "once", "here", "there", "when", "where", "why", "how",
    "both", "few", "many", "much", "very", "just", "also", "well",
}


@lru_cache(maxsize=128)
def get_embedding(text):
    return model.encode(text, convert_to_tensor=True)


def _tokenize(text):
    """Extract meaningful words: lowercased, alphanumeric, length >= 3, no stopwords."""
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.\-]{2,}\b", text.lower())
    return {w for w in words if w not in STOPWORDS}


def keyword_match_score(resume_text, jd_text):
    # Semantic similarity
    resume_embedding = get_embedding(resume_text)
    jd_embedding = get_embedding(jd_text)
    similarity_score = util.cos_sim(resume_embedding, jd_embedding).item()
    keyword_score = int(similarity_score * 100)

    # Cleaned missing keywords (no stopwords, no short junk)
    resume_words = _tokenize(resume_text)
    jd_words = _tokenize(jd_text)
    missing = sorted(jd_words - resume_words)

    return keyword_score, similarity_score, missing[:10]