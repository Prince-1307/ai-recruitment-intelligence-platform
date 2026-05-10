from modules.basic_roles import (
    BASIC_ROLES
)


def update_roles(role):

    existing = set(

        [r.lower() for r in BASIC_ROLES]

    )

    if role.lower() not in existing:

        BASIC_ROLES.append(role)

        with open(
            "modules/basic_roles.py",
            "w"
        ) as f:

            f.write("BASIC_ROLES = [\n\n")

            for r in sorted(BASIC_ROLES):

                f.write(
                    f'    "{r}",\n'
                )

            f.write("\n]")
            