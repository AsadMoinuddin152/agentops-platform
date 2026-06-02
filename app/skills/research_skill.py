from app.core.ollama_client import ask_llm


NAME = "research_skill"

CAPABILITIES = [
    "what",
    "why",
    "explain",
    "research",
    "learn",
    "concept"
]

DEPENDENCIES = [
    "rag_skill"
]


def extract_context(context):

    gathered = []

    if not context:
        return ""

    for item in context:

        if (
            isinstance(item, dict)
            and item.get("rag_context")
        ):

            gathered.append(
                item["rag_context"]
            )

    return "\n\n".join(
        gathered
    )


def execute(
    user_input,
    context=None
):

    rag_context = extract_context(
        context
    )

    prompt = f"""
Research task:

User:
{user_input}

Semantic Context:
{rag_context}
"""

    result = ask_llm(prompt)

    return {
        "skill":
            NAME,
        "thoughts": [
            "Retrieved semantic context",
            "Performed research reasoning"
        ],
        "result":
            result
    }