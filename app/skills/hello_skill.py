NAME = "hello_skill"

CAPABILITIES = [
    "hello"
]


def execute(
    user_input,
    context=None
):

    return {
        "skill": NAME,
        "result":
            "Hello from plugin skill"
    }