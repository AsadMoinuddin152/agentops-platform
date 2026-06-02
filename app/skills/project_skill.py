from app.core.ollama_client import ask_llm


NAME = "project_skill"

CAPABILITIES = [
    "project",
    "setup",
    "architecture",
    "analyze",
    "system"
]

DEPENDENCIES = [
    "rag_skill"
]


def extract_rag_context(context):

    if not context:
        return "", []

    rag_context = ""
    retrieved_files = []

    for item in context:

        if (
            isinstance(item, dict)
            and item.get("rag_context")
        ):

            rag_context = item[
                "rag_context"
            ]

            retrieved_files = item.get(
                "retrieved_files",
                []
            )

    return (
        rag_context,
        retrieved_files
    )


def execute(
    user_input,
    context=None
):

    text = user_input.lower()

    if not any(
        word in text
        for word in CAPABILITIES
    ):
        return None

    rag_context, files = extract_rag_context(
        context
    )

    prompt = f"""
You are performing CODE REVIEW.

ONLY use retrieved code.

NEVER invent:
- functions
- classes
- pipelines
- infrastructure
- Kubernetes
- examples

If code is missing, say:
"Not present in retrieved code."

Retrieved files:
{files}

Retrieved code:
{rag_context}

Task:
{user_input}

Required output:

1. Files involved
2. Orchestrator flow
3. Agent routing
4. Skill loading
5. Dependency execution
6. Telemetry/logging
7. rag_skill role
8. End-to-end request flow

Use only retrieved implementation.
"""

    result = ask_llm(
        prompt
    )

    return {
        "skill":
            NAME,
        "thoughts": [
            "Reviewed retrieved code",
            "Grounded reasoning",
            "Generated architecture summary"
        ],
        "result":
            result
    }