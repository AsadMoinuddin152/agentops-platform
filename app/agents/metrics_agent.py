from app.skills.registry import SKILLS
from app.skills.router import (
    find_best_skill
)
from app.skills.executor import (
    execute_skill_chain
)
from app.core.response_formatter import (
    format_response
)

NAME = "metrics"

CAPABILITIES = [
    "metrics",
    "telemetry",
    "performance",
    "logs",
    "analytics"
]


def execute(user_input):

    allowed_skills = list(
        SKILLS.keys()
    )

    (
        selected_skill,
        reasons
    ) = find_best_skill(
        user_input,
        allowed_skills
    )

    if not selected_skill:

        from app.core.ollama_client import ask_llm
        result = ask_llm(
            f"""
            System Performance query:

            {user_input}
            """
        )
        chain = []

    else:

        result, chain = execute_skill_chain(
            selected_skill,
            user_input
        )

    return format_response(
        "Metrics Agent",
        user_input,
        result,
        {
            "selected_skill":
                selected_skill,

            "skill_reason":
                reasons,

            "skill_chain":
                chain
        }
    )
