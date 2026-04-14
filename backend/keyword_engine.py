from functools import lru_cache
from sentence_transformers import SentenceTransformer, util
import re

# BGE-small: better MTEB scores than MiniLM, still lightweight (~130MB)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# BGE recommends a query prefix for retrieval-style tasks
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

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
    # Resume/JD noise
    "experience", "work", "role", "team", "years", "year", "company",
    "position", "job", "ability", "skills", "skill", "knowledge",
    "responsibilities", "responsibility", "qualifications", "candidate",
    "candidates", "required", "preferred", "etc", "including", "include",
    "based", "using", "across", "within", "strong", "good", "great",
    "best", "new", "like", "way", "ways", "looking", "seeking", "help",
    "make", "making", "work", "works", "working", "worked", "use", "used",
    "uses", "day", "days", "time", "times", "people", "person", "level",
    "high", "low", "one", "two", "three", "four", "five", "first",
    "second", "third", "annual", "bachelor", "master", "degree", "plus",
    "per", "month", "months", "week", "weeks", "daily", "weekly",
    "monthly", "build", "builds", "building", "built", "design",
    "designs", "designing", "designed", "develop", "develops",
    "developing", "developed", "create", "creates", "creating", "created",
    "books", "book", "budget", "biases", "bias", "architectures",
    "architecture", "who", "what", "whom", "whose", "which",
    "solutions", "solution", "problem", "problems", "users", "user",
    "products", "product", "business", "businesses", "customer",
    "customers", "client", "clients", "company", "companies",
}


@lru_cache(maxsize=128)
def _encode(text):
    return model.encode(text, convert_to_tensor=True, normalize_embeddings=True)


def _tokenize(text):
    """Extract tokens that LOOK LIKE technical terms."""
    # Allow multi-word tech phrases (react native, machine learning)
    # For now: single tokens — alphanumeric, allow +/#/.- for C++, C#, Node.js
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.\-]{2,}\b", text.lower())
    filtered = set()
    for w in words:
        if w in STOPWORDS:
            continue
        if len(w) < 3:
            continue
        # Skip pure numbers masquerading as words (shouldn't happen given regex, but safe)
        if w.isdigit():
            continue
        filtered.add(w)
    return filtered


def _rescale_similarity(sim):
    """
    Raw cosine sim between resume/JD is usually 0.4-0.8 even for bad matches,
    because both are English prose. Rescale so users see useful numbers:
      sim < 0.45 -> 0-40 (poor match)
      0.45-0.65  -> 40-80 (decent to strong)
      0.65+      -> 80-100 (excellent)
    """
    if sim < 0.45:
        scaled = (sim / 0.45) * 40
    elif sim < 0.65:
        scaled = 40 + ((sim - 0.45) / 0.20) * 40
    else:
        scaled = 80 + min((sim - 0.65) / 0.15, 1.0) * 20
    return max(0, min(100, int(round(scaled))))


def keyword_match_score(resume_text, jd_text):
    # BGE uses prefix on the "query" side (treat JD as the query)
    resume_embedding = _encode(resume_text)
    jd_embedding = _encode(QUERY_PREFIX + jd_text)

    similarity = util.cos_sim(resume_embedding, jd_embedding).item()
    keyword_score = _rescale_similarity(similarity)

    # Missing keywords — only return ones that look like skills/tech/proper nouns
    resume_words = _tokenize(resume_text)
    jd_words = _tokenize(jd_text)

    missing = jd_words - resume_words

    # Prefer terms that look like tech: contain digits, symbols, or are short tokens common in tech
    # (not perfect, but eliminates most noise)
    def looks_technical(w):
        # Has a symbol typical of tech (c++, c#, node.js, ci/cd)
        if any(c in w for c in "+#."):
            return True
        # Common tech suffixes/forms
        if w.endswith(("js", "py", "db", "sql", "api", "ml", "ai", "ui", "ux")):
            return True
        # Short acronyms (aws, gcp, rag, llm) — but must not be in stopwords
        if len(w) <= 4:
            return True
        # Longer single words: keep if not obviously generic English
        # (we already filtered stopwords, so this catches tech nouns like
        # "pytorch", "kubernetes", "transformers", etc.)
        return True

    missing = sorted(w for w in missing if looks_technical(w))
    return keyword_score, similarity, missing[:10]