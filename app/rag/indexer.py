import os
import uuid

from app.rag.chunker import chunk_text
from app.rag.embedder import embed_text
from app.rag.chroma_client import collection
from app.core.config import PROJECT_PATH


INCLUDE_DIRS = [
    "agents",
    "skills",
    "core",
    "tools",
    "api"
]

SKIP_FILES = [
    "__init__.py"
]


def should_index(root, file):

    if file in SKIP_FILES:
        return False

    if not file.endswith(".py"):
        return False

    relative = os.path.relpath(
        root,
        PROJECT_PATH
    )

    top = relative.split(
        os.sep
    )[0]

    return top in INCLUDE_DIRS


def index_project():

    try:

        collection.delete(
            where={}
        )

    except:
        pass

    for root, _, files in os.walk(
        PROJECT_PATH
    ):

        for file in files:

            if not should_index(
                root,
                file
            ):
                continue

            filepath = os.path.join(
                root,
                file
            )

            try:

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as f:

                    text = f.read()

                chunks = chunk_text(
                    text
                )

                for i, chunk in enumerate(
                    chunks
                ):

                    embedding = embed_text(
                        chunk
                    )

                    collection.add(
                        ids=[
                            str(
                                uuid.uuid4()
                            )
                        ],
                        embeddings=[
                            embedding
                        ],
                        documents=[
                            chunk
                        ],
                        metadatas=[{
                            "file":
                                file,
                            "path":
                                filepath,
                            "chunk":
                                i
                        }]
                    )

                print(
                    f"Indexed {filepath}"
                )

            except Exception as e:

                print(
                    f"Failed {filepath}: {e}"
                )


if __name__ == "__main__":

    index_project()