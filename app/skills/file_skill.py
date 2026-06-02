from app.tools.tool_registry import TOOLS


NAME = "file_skill"

CAPABILITIES = [
    "file",
    "read",
    ".py",
    ".txt",
    "dockerfile",
    "requirements"
]

DEPENDENCIES = []


def execute(
    user_input,
    context=None
):

    files = TOOLS[
        "list_files"
    ]().split("\n")

    gathered = []

    for filename in [
        "Dockerfile",
        "requirements.txt",
        ".env"
    ]:

        if filename in files:

            content = TOOLS[
                "read_file"
            ](filename)

            gathered.append(
                f"{filename}:\n{content}"
            )

    # explicit read file

    if user_input.lower().startswith(
        "read file"
    ):

        filename = user_input.replace(
            "read file",
            ""
        ).strip()

        result = TOOLS[
            "read_file"
        ](filename)

        return {
            "skill": NAME,
            "result": result
        }

    # dependency provider

    return {
        "skill": NAME,
        "context": gathered
    }