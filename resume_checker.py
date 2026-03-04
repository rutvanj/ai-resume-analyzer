def analyze_resume(resume, job_desc):

    resume = resume.lower()
    job_desc = job_desc.lower()

    skills = [
        "python","machine learning","sql","tensorflow","pandas",
        "numpy","java","c++","aws","docker","kubernetes"
    ]

    resume_skills = []
    job_skills = []

    for skill in skills:
        if skill in resume:
            resume_skills.append(skill)

        if skill in job_desc:
            job_skills.append(skill)

    matched = []

    for skill in job_skills:
        if skill in resume_skills:
            matched.append(skill)

    missing = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)

    if len(job_skills) > 0:
        match_score = int((len(matched) / len(job_skills)) * 100)
    else:
        match_score = 0

    resume_score = min(len(resume_skills) * 10, 100)

    return {
        "resume_score": resume_score,
        "match_score": match_score,
        "skills": resume_skills,
        "missing": missing
    }