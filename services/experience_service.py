import re
from sklearn.metrics.pairwise import cosine_similarity
from services.embedding_service import get_embeddings

def extract_experience_sentences(text):
    sentences = re.split(r'\.|\n', text)
    exp_sentences = [s for s in sentences if "year" in s.lower()]
    return " ".join(exp_sentences)


def experience_relevance_score(job_desc, resume_text):
    exp_text = extract_experience_sentences(resume_text)

    if not exp_text.strip():
        return 0

    embeddings = get_embeddings([job_desc, exp_text])
    similarity = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]

    return float(round(similarity, 4))