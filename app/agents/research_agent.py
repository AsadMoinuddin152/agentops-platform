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

NAME = "research"

CAPABILITIES = [
    "explain",
    "research",
    "concept",
    "learn",
    "what",
    "why",
    "kubernetes",
    "ai"
]

RESEARCH_SKILLS = [
    "research_skill"
]


def research_agent(user_input):

    (
        selected_skill,
        reasons
    ) = find_best_skill(
        user_input,
        RESEARCH_SKILLS
    )

    if not selected_skill:

        from app.core.ollama_client import ask_llm
        result = ask_llm(user_input)
        chain = []

    else:

        result, chain = execute_skill_chain(
            selected_skill,
            user_input
        )

    return format_response(
        "Research Agent",
        user_input,
        result,
        {
            "selected_skill":
                selected_skill,
            "skill_reason":
                reasons,
        }
    )


execute = research_agent