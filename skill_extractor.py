import re

def load_skills():

    with open("skills.txt", "r") as f:
        skills = [skill.strip().lower() for skill in f.readlines()]

    return skills


def extract_skills(text, skills_db):

    text = text.lower()

    found_skills = []

    for skill in skills_db:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))