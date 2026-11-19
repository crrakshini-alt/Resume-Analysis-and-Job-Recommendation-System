
from skill_gap_analysis import JOB_ROLES, analyze_skill_gap


def recommend_job_roles(candidate_skills):

    recommendations = []

    # Check all available job roles
    for job_role in JOB_ROLES:

        result = analyze_skill_gap(
            candidate_skills,
            job_role
        )

        recommendations.append(result)

    # Sort roles by highest skill match
    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return recommendations
