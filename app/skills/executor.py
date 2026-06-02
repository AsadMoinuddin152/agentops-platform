


import time
from app.skills.registry import SKILLS
from app.core.metrics import log_metric
from app.tools.tool_registry import track_tool


def execute_skill_chain(
    skill_name,
    user_input
):

    chain = []
    context = []
    skill_durations = {}
    dependency_count = 0

    visited = set()

    chain_start = time.time()

    def run(skill):

        nonlocal dependency_count

        if skill in visited:
            return

        visited.add(
            skill
        )

        deps = SKILLS[
            skill
        ].get(
            "dependencies",
            []
        )

        for dep in deps:

            dependency_count += 1
            run(dep)

        skill_start = time.time()

        track_tool(f"skill:{skill}")

        result = SKILLS[
            skill
        ]["handler"](
            user_input,
            context
        )

        skill_durations[skill] = round(
            (time.time() - skill_start) * 1000,
            2
        )

        if result:

            chain.append(
                skill
            )

            # keep structured context

            if isinstance(
                result,
                dict
            ):

                context.append(
                    result
                )

            else:

                context.append({
                    "result":
                        str(result)
                })

        return result

    final = run(
        skill_name
    )

    total_chain_duration_ms = round(
        (time.time() - chain_start) * 1000,
        2
    )

    # Emit skill chain metrics
    log_metric(
        component="skill",
        event="skill_chain",
        data={
            "skill_chain":
                chain,
            "skill_durations_ms":
                skill_durations,
            "total_chain_duration_ms":
                total_chain_duration_ms,
            "dependency_count":
                dependency_count
        }
    )

    return (
        final,
        chain
    )