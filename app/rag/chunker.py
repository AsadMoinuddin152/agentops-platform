from app.core.config import CHUNK_LINES, CHUNK_OVERLAP


def chunk_text(
    text,
    chunk_lines=CHUNK_LINES,
    overlap=CHUNK_OVERLAP
):

    lines = text.splitlines()

    chunks = []

    start = 0

    while start < len(lines):

        end = start + chunk_lines

        chunk = "\n".join(
            lines[start:end]
        )

        if chunk.strip():

            chunks.append(
                chunk
            )

        start += (
            chunk_lines
            - overlap
        )

    return chunks