from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from semantic_engine import semantic_similarity_score


def keyword_match_score(resume_text, jd_text):

    # ---- TF-IDF similarity ----
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])

    tfidf_similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    # ---- Semantic similarity ----
    semantic_score, semantic_similarity = semantic_similarity_score(
        resume_text,
        jd_text
    )

    # ---- Hybrid similarity ----
    hybrid_similarity = (0.4 * tfidf_similarity) + (0.6 * semantic_similarity)

    keyword_score = round(hybrid_similarity * 100, 2)

    missing_keywords = find_missing_keywords(vectorizer, vectors)

    return keyword_score, hybrid_similarity, missing_keywords


def find_missing_keywords(vectorizer, vectors):

    feature_names = np.array(vectorizer.get_feature_names_out())

    jd_vector = vectors[1].toarray()[0]
    resume_vector = vectors[0].toarray()[0]

    important_indices = jd_vector.argsort()[-50:]

    missing = []

    # Generic non-technical words
    generic_words = [
        "looking", "developer", "experience", "skills",
        "knowledge", "team", "work", "strong",
        "candidate", "applications", "backend",
        "cloud", "ci", "cd", "deploying",
        "preferred", "plus", "services",
        "building", "using", "should",
        "familiarity", "development",
        "engineer", "software", "practices",
        "databases", "pipelines"
    ]

    # Basic technical indicator keywords
    tech_indicators = [
        "python", "java", "c++", "sql",
        "fastapi", "flask", "django",
        "docker", "kubernetes", "aws",
        "tensorflow", "pytorch",
        "scikit", "redis", "postgres",
        "mongodb", "azure", "gcp",
        "spark", "hadoop", "api"
    ]

    for idx in important_indices:
        word = feature_names[idx]

        if (
            resume_vector[idx] == 0
            and word not in generic_words
            and len(word) > 3
        ):

            # Only keep tech-like words
            if any(tech in word for tech in tech_indicators):
                missing.append(word)

    missing = list(dict.fromkeys(missing))

    return missing[:8]