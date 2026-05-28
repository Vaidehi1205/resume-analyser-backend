import json

with open("skills.json", "r") as f:
    SKILLS = json.load(f)

def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))