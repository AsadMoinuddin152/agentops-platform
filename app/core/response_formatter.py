def format_response(
    agent,
    task,
    result,
    metadata=None
):

    response = {
        "agent": agent,
        "task": task,
        "result": result
    }

    if metadata:

        response[
            "metadata"
        ] = metadata

    return response