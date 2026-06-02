NAME = "hi_skill"

CAPABILITIES = [
    "hi",
    "hey",
    "greetings",
    "hi there"
]


def execute(
    user_input,
    context=None
):

    return {
        "skill": NAME,
        "result":
            "Hi from plugin skill"
    }