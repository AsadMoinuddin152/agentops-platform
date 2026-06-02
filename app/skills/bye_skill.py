NAME = "bye_skill"

CAPABILITIES = [
    "bye"
]


def execute(
    user_input,
    context=None
):

    return {
        "skill": NAME,
        "result":
            "Bye from plugin skill"
    }