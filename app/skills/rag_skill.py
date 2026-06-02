from app.rag.embedder import embed_text
from app.rag.chroma_client import collection
from app.core.metrics import log_metric
from app.core.config import RAG_N_RESULTS
import time


NAME = "rag_skill"

DESCRIPTION = "Semantic project retrieval"

CAPABILITIES = [
    "semantic_search",
    "context_retrieval",
    "rag"
]

DEPENDENCIES = []


ARCH_FILES = [
    "orchestrator.py",
    "registry.py",
    "executor.py",
    "router.py",
    "project_skill.py",
    "rag_skill.py",
    "telemetry.py"
]


def dedupe(items):

    seen = set()
    result = []

    for item in items:

        key = item.strip()

        if key and key not in seen:

            seen.add(key)
            result.append(item)

    return result


def build_query(user_input):

    text = user_input.lower()

    if any(
        k in text
        for k in [
            "architecture",
            "project",
            "system"
        ]
    ):

        return (
            user_input
            + " orchestrator agent router skill registry executor telemetry rag"
        )

    return user_input


def score_file(name):

    if name in ARCH_FILES:
        return 10

    return 0


def execute(
    user_input,
    context=None
):

    query = build_query(
        user_input
    )

    rag_start = time.time()

    embedding = embed_text(
        query
    )

    # Query Chroma DB with n_results=RAG_N_RESULTS for comprehensive context
    results = collection.query(
        query_embeddings=[
            embedding
        ],
        n_results=RAG_N_RESULTS
    )

    retrieval_duration_ms = round(
        (time.time() - rag_start) * 1000,
        2
    )

    docs = results.get(
        "documents",
        [[]]
    )[0]

    meta = results.get(
        "metadatas",
        [[]]
    )[0]

    paired = []

    for i, doc in enumerate(docs):

        file_name = "unknown"

        if i < len(meta) and meta[i]:
            file_name = meta[i].get(
                "file",
                "unknown"
            )

        paired.append(
            (
                score_file(
                    file_name
                ),
                file_name,
                doc
            )
        )

    paired.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    blocks = []

    seen = set()

    for _, file_name, doc in paired:

        key = doc.strip()

        if key in seen:
            continue

        seen.add(key)

        blocks.append(
            f"""
FILE: {file_name}

CODE:
{doc}
"""
        )

    merged = "\n\n==========\n\n".join(
        blocks
    )

    unique_files = list(
        set([p[1] for p in paired])
    )

    top_files = [
        p[1] for p in paired[:5]
    ]

    # Emit RAG retrieval metrics
    log_metric(
        component="rag",
        event="rag_query",
        data={
            "query_length":
                len(query),
            "vector_hits":
                len(blocks),
            "unique_files_count":
                len(unique_files),
            "unique_files":
                unique_files,
            "top_files":
                top_files,
            "retrieval_duration_ms":
                retrieval_duration_ms
        }
    )

    return {
        "rag_context":
            merged,
        "vector_hits":
            len(blocks),
        "retrieved_files":
            unique_files
    }