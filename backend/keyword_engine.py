from functools import lru_cache
from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
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
    "experience", "work", "role", "team", "years", "year", "company",
    "position", "job", "ability", "skills", "skill", "knowledge",
    "responsibilities", "responsibility", "qualifications", "candidate",
    "candidates", "required", "preferred", "etc", "including", "include",
    "based", "using", "across", "within", "strong", "good", "great",
    "best", "new", "like", "way", "ways", "looking", "seeking", "help",
    "make", "making", "works", "working", "worked", "use", "used",
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
    "customers", "client", "clients", "companies",
    # Additional noise observed in real output
    "closely", "close", "code", "codes", "coding", "classification",
    "classifications", "class", "classes", "clean", "cleaning", "real",
    "world", "worlds", "top", "tier", "hands", "hand", "learn",
    "learning", "learned", "learns", "understanding", "understand",
    "work-from-home", "remote", "office", "hybrid", "full", "part",
    "fulltime", "parttime", "senior", "junior", "mid", "entry",
    "opportunity", "opportunities", "culture", "environment",
    "flexible", "competitive", "offer", "offers", "offering", "benefits",
    "benefit", "salary", "equity", "stock", "bonus", "bonuses",
    "insurance", "health", "dental", "vision", "pto", "vacation",
    "holiday", "holidays", "role", "roles", "team", "teams",
    "critical", "key", "core", "major", "minor", "ideal", "desired",
    "typical", "typically", "closely", "regularly", "consistently",
    "effectively", "efficiently", "quickly", "slowly", "easily",
    "write", "writes", "writing", "written", "read", "reads",
    "reading", "ensure", "ensures", "ensuring", "ensured",
    "iterate", "iterates", "iterating", "iterated", "feedback",
    "review", "reviews", "reviewing", "reviewed", "release",
    "releases", "releasing", "released", "participate", "participates",
    "participating", "participated", "part", "parts", "join", "joins",
    "joining", "joined", "grow", "grows", "growing", "grew",
    "impact", "impacts", "impactful", "drive", "drives", "driving",
    "driven", "expand", "expanding", "expanded", "contribute",
    "contributes", "contributing", "contributed", "needs", "need",
    "wants", "want", "desire", "desires", "cutting", "edge",
    "latest", "modern", "innovative", "innovation", "innovations",
    "quality", "performance", "scale", "scaling", "scaled",
    "result", "results", "resulting", "resulted", "value", "values",
    "valued", "valuing", "effective", "efficient", "proficient",
    "proficiency", "expert", "expertise", "fluent", "familiar",
    "familiarity", "passion", "passionate", "motivated", "self",
    "driven", "ownership", "autonomy", "leadership", "lead", "leads",
    "mentor", "mentoring", "mentored", "mentors", "manage", "manages",
    "managing", "managed", "communicate", "communicates",
    "communicating", "communicated", "communication",
    "communications", "collaborate", "collaborating", "collaborated",
    "collaboration", "collaborative",
}


@lru_cache(maxsize=128)
def _encode(text):
    return model.encode(text, convert_to_tensor=True, normalize_embeddings=True)


def _tokenize(text):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.\-]{2,}\b", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) >= 3 and not w.isdigit()}


def _rescale_similarity(sim):
    if sim < 0.45:
        scaled = (sim / 0.45) * 40
    elif sim < 0.65:
        scaled = 40 + ((sim - 0.45) / 0.20) * 40
    else:
        scaled = 80 + min((sim - 0.65) / 0.15, 1.0) * 20
    return max(0, min(100, int(round(scaled))))


def _looks_technical(w):
    """Heuristic: does this word look like a skill/tech term rather than generic English?"""
    # Has a tech symbol (c++, c#, node.js, ci/cd)
    if any(c in w for c in "+#."):
        return True
    # Common tech-form suffixes
    if w.endswith(("js", "py", "db", "sql", "api", "apis", "ml", "ai", "ui", "ux", "ops")):
        return True
    # Short acronyms (already stopword-filtered, so these are likely tech)
    if len(w) <= 4:
        return True
    # Longer words — only keep if they end in letters that suggest tech (not generic English)
    # This filters out "closely", "classification", "understanding" etc.
    # Heuristic: tech terms rarely end in -ly, -tion, -ing, -ed, -ment, -ness
    generic_suffixes = ("ly", "tion", "ment", "ness", "ship", "able", "ible", "ward")
    if any(w.endswith(suf) for suf in generic_suffixes):
        return False
    return True


def keyword_match_score(resume_text, jd_text):
    resume_embedd