import re
from app.skills.registry import SKILLS


def find_best_skill(
    user_input,
    allowed_skills
):

    text = user_input.lower()

    scores = {}
    reasons = {}

    for skill_name in allowed_skills:

        config = SKILLS[
            skill_name
        ]

        score = 0
        matched = []

        for capability in config["capabilities"]:
            pattern = rf"\b{re.escape(capability.lower())}\b"
            if re.search(pattern, text):
                score += 1
                matched.append(capability)



        scores[
            skill_name
        ] = score

        reasons[
            skill_name
        ] = matched

    best_skill = max(
        scores,
        key=scores.get
    )

    if scores[
        best_skill
    ] == 0:

        return (
            None,
            []
        )

    return (
        best_skill,
        reasons[
            best_skill
        ]
    )