import re

SKILL_TAXONOMY = {
    # Languages
    "python": "Python", "java": "Java", "javascript": "JavaScript",
    "typescript": "TypeScript", "c++": "C++", "c#": "C#",
    "golang": "Go", " go ": "Go", "ruby": "Ruby", "rust": "Rust",
    "kotlin": "Kotlin", "swift": "Swift", "php": "PHP", "scala": "Scala",
    "r ": "R", "matlab": "MATLAB", "sql": "SQL", "bash": "Bash",
    "shell": "Shell scripting",

    # Frontend
    "react.js": "React", "reactjs": "React", "react native": "React Native",
    "react": "React", "next.js": "Next.js", "nextjs": "Next.js",
    "vue.js": "Vue", "vuejs": "Vue", "vue": "Vue", "angular": "Angular",
    "svelte": "Svelte", "tailwind": "Tailwind CSS", "html": "HTML",
    "css": "CSS", "sass": "Sass", "redux": "Redux",

    # Backend
    "node.js": "Node.js", "nodejs": "Node.js", "express": "Express",
    "fastapi": "FastAPI", "flask": "Flask", "django": "Django",
    "spring boot": "Spring Boot", "spring": "Spring", ".net": ".NET",
    "dotnet": ".NET", "ruby on rails": "Ruby on Rails", "rails": "Rails",
    "graphql": "GraphQL", "rest api": "REST APIs", "grpc": "gRPC",

    # ML / AI / Data
    "machine learning": "Machine Learning", "deep learning": "Deep Learning",
    "natural language processing": "NLP", "nlp": "NLP",
    "computer vision": "Computer Vision", "pytorch": "PyTorch",
    "tensorflow": "TensorFlow", "keras": "Keras",
    "scikit-learn": "scikit-learn", "sklearn": "scikit-learn",
    "pandas": "Pandas", "numpy": "NumPy",
    "hugging face": "Hugging Face", "huggingface": "Hugging Face",
    "transformers": "Transformers", "langchain": "LangChain",
    "llamaindex": "LlamaIndex", "openai": "OpenAI API",
    "llm": "LLMs", "llms": "LLMs", "rag": "RAG",
    "vector database": "Vector databases", "pinecone": "Pinecone",
    "weaviate": "Weaviate", "faiss": "FAISS", "chromadb": "ChromaDB",
    "mlflow": "MLflow", "wandb": "Weights & Biases",
    "weights & biases": "Weights & Biases", "kubeflow": "Kubeflow",
    "airflow": "Airflow", "spark": "Spark", "kafka": "Kafka",
    "hadoop": "Hadoop",

    # Cloud / DevOps
    "aws": "AWS", "amazon web services": "AWS", "azure": "Azure",
    "gcp": "GCP", "google cloud": "GCP", "docker": "Docker",
    "kubernetes": "Kubernetes", "k8s": "Kubernetes",
    "terraform": "Terraform", "ansible": "Ansible", "jenkins": "Jenkins",
    "github actions": "GitHub Actions", "ci/cd": "CI/CD",
    "gitlab ci": "GitLab CI", "circleci": "CircleCI", "linux": "Linux",
    "nginx": "Nginx",

    # Databases
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL",
    "mysql": "MySQL", "mongodb": "MongoDB", "redis": "Redis",
    "elasticsearch": "Elasticsearch", "dynamodb": "DynamoDB",
    "cassandra": "Cassandra", "snowflake": "Snowflake",
    "bigquery": "BigQuery",

    # Tools / misc
    "git": "Git", "github": "GitHub", "gitlab": "GitLab",
    "jira": "Jira", "agile": "Agile", "scrum": "Scrum", "figma": "Figma",
}


def _find_skills(text):
    text_padded = " " + text.lower() + " "
    found = set()
    for alias in sorted(SKILL_TAXONOMY.keys(), key=len, reverse=True):
        if len(alias) <= 3 or alias.startswith(" ") or alias.endswith(" "):
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias.strip()) + r"(?![a-zA-Z0-9])"
        else:
            pattern = re.escape(alias)
        if re.search(pattern, text_padded):
            found.add(SKILL_TAXONOMY[alias])
    return found


def calculate_skills_score(resume_text, jd_text):
    jd_skills = _find_skills(jd_text)
    if not jd_skills:
        return 50, [], {"matched": [], "total_jd_skills": 0, "matched_count": 0}

    resume_skills = _find_skills(resume_text)
    matched = jd_skills & resume_skills
    missing = jd_skills - resume_skills

    ratio = len(matched) / len(jd_skills)
    score = int(round(ratio * 100))

    stats = {
        "matched": sorted(matched),
        "total_jd_skills": len(jd_skills),
        "matched_count": len(matched),
    }

    return score, sorted(missing), stats