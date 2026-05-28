from sklearn.metrics.pairwise import cosine_similarity
from services.embedding_service import get_embeddings
from services.skill_service import skill_match_score
from services.experience_service import experience_relevance_score


def compute_scores(job_desc, resume_text):

    # Semantic similarity
    embeddings = get_embeddings([job_desc, resume_text])
    similarity = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]

    # Skill match
    skill_percent, matched_skills = skill_match_score(job_desc, resume_text)

    # Experience relevance
    exp_score = experience_relevance_score(job_desc, resume_text)

    # Weighted Final Score
    final_score = (
        0.5 * similarity +
        0.3 * (skill_percent / 100) +
        0.2 * exp_score
    )

    return {
        "similarity_score": round(float(similarity), 4),
        "skill_match_percent": round(skill_percent, 2),
        "matched_skills": matched_skills,
        "experience_relevance": exp_score,
        "final_score": round(float(final_score), 4)
    }