import spacy
import json
from spacy.pipeline import EntityRuler

# ==================================================
# LOAD MODEL
# ==================================================

nlp = spacy.load("en_core_web_sm")

# ==================================================
# LOAD SKILLS
# ==================================================

with open("skills.json", "r") as f:

    SKILLS = json.load(f)

# ==================================================
# ENTITY RULER
# ==================================================

ruler = nlp.add_pipe(
    "entity_ruler",
    before="ner"
)

patterns = []

for skill in SKILLS:

    patterns.append({

        "label": "SKILL",

        "pattern": skill
    })

ruler.add_patterns(patterns)

# ==================================================
# EXTRACT SKILLS
# ==================================================

def extract_skills(text):

    doc = nlp(text)

    skills = set()

    for ent in doc.ents:

        if ent.label_ == "SKILL":

            skills.add(
                ent.text.lower()
            )

    return list(skills)
