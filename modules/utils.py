def calculate_ats_score(

    resume_skills,

    job_skills

):

    resume_set = set(
        [s.lower() for s in resume_skills]
    )

    job_set = set(
        [s.lower() for s in job_skills]
    )

    matched = resume_set.intersection(
        job_set
    )

    missing = job_set.difference(
        resume_set
    )

    ats_score = (

        len(matched)

        / len(job_set)

    ) * 100 if len(job_set) > 0 else 0

    return ats_score, matched, missing