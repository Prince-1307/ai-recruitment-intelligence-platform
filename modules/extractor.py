from modules.skills import SKILLS

from modules.cleaner import clean_text


def extract_skills(text):

    text = clean_text(text)

    found = []

    for skill in SKILLS:

        if skill.lower() in text:

            found.append(skill)

    return list(set(found))