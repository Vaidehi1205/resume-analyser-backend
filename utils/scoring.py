def calculate_match_score(similarity, matched_skills, total_required_skills):
    semantic_score = similarity * 100

    if total_required_skills == 0:
        skill_score = 0
    else:
        skill_score = (
                              len(matched_skills) / total_required_skills
                      ) * 100

    final_score = (
            0.6 * semantic_score +
            0.4 * skill_score
    )

    return round(final_score, 2)