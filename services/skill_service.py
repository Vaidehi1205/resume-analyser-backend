import re

# Common words to ignore
STOPWORDS = {
    "the", "and", "for", "with", "a", "an", "to", "of",
    "in", "on", "at", "by", "is", "are", "be", "will",
    "developer", "engineer", "experience", "knowledge",
    "working", "good", "strong", "ability", "team",
    "candidate", "skills", "required", "preferred"
}


def extract_skills_from_jd(job_desc):

    # Extract words + technologies
    words = re.findall(r"[A-Za-z0-9\+\#\.]+", job_desc.lower())

    # Remove stopwords and short words
    skills = []

    for word in words:
        if word not in STOPWORDS and len(word) > 2:
            skills.append(word)

    return list(set(skills))


def extract_resume_matches(job_skills, resume_text):

    resume_text = resume_text.lower()

    matched = []

    for skill in job_skills:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, resume_text):
            matched.append(skill)

    return matched


def skill_match_score(job_desc, resume_text):

    # Dynamically extract skills from JD
    job_skills = extract_skills_from_jd(job_desc)

    # Match against resume
    matched_skills = extract_resume_matches(
        job_skills,
        resume_text
    )

    # Percentage
    percent = (
        len(matched_skills) / len(job_skills) * 100
        if job_skills else 0
    )

    return {
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "skill_match_percent": round(percent, 2)
    }