def load_skills():
    with open("skills.txt","r") as f:
        skills = f.read().splitlines()
    return skills


def extract_skills(text, skills_db):
    
    text = text.lower()
    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return found_skills