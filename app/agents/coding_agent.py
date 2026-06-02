from app.skills.registry import SKILLS
from app.skills.router import (
    find_best_skill
)
from app.skills.executor import (
    execute_skill_chain
)
from app.core.ollama_client import ask_llm
from app.core.response_formatter import (
    format_response
)

NAME = "coding"

CAPABILITIES = [
    "file",
    "code",
    "debug",
    "python",
    "docker",
    "project",
    "setup",
    "architecture",
    "analyze"
]


def coding_agent(user_input):

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

        result = ask_llm(
            f"""
            Coding task:

            {user_input}
            """
        )

        return format_response(
            "Coding Agent",
            user_input,
            result
        )

    result, chain = (
        execute_skill_chain(
            selected_skill,
            user_input
        )
    )

    return format_response(
        "Coding Agent",
        user_input,
        result,
        {
            "selected_skill":
                selected_skill,

            "skill_reason":
                reasons,

        }
    )


execute = coding_agent