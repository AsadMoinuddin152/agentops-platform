from datetime import datetime
import os


TOOL_TRACE = []


def track_tool(name):

    TOOL_TRACE.append(name)


def get_tool_trace():

    tools = TOOL_TRACE.copy()

    TOOL_TRACE.clear()

    return tools


def get_time():

    track_tool("time")

    return str(datetime.now())


def list_files():

    track_tool("list_files")

    files = os.listdir(".")

    return "\n".join(files)


def read_file(filename):

    track_tool(
        f"read_file:{filename}"
    )

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    except Exception as e:

        return str(e)


def get_env():

    track_tool("get_env")

    from app.core.config import MODEL, EMBEDDING_MODEL, CHROMA_COLLECTION, RAG_N_RESULTS, MEMORY_LIMIT

    return (
        f"Active configuration parameters:\n"
        f"- Model: {MODEL}\n"
        f"- Embedder: {EMBEDDING_MODEL}\n"
        f"- Database Collection: {CHROMA_COLLECTION}\n"
        f"- RAG retrieval size: {RAG_N_RESULTS}\n"
        f"- Memory limit: {MEMORY_LIMIT}"
    )


TOOLS = {
    "time": get_time,
    "list_files": list_files,
    "read_file": read_file,
    "get_env": get_env
}