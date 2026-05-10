from modules.skills import SKILLS


def update_skills(new_skills):

    existing = set(
        [s.lower() for s in SKILLS]
    )

    updated = False

    for skill in new_skills:

        if skill.lower() not in existing:

            SKILLS.append(skill)

            updated = True

    if updated:

        with open(
            "modules/skills.py",
            "w"
        ) as f:

            f.write("SKILLS = [\n\n")

            for skill in sorted(SKILLS):

                f.write(
                    f'    "{skill}",\n'
                )

            f.write("\n]")