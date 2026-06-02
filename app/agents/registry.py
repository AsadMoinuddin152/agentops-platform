import os
import importlib

AGENTS = {}


def load_agents():

    agents_dir = "app/agents"

    for file in os.listdir(
        agents_dir
    ):

        if (
            file.endswith(
                "_agent.py"
            )
            and file != "__init__.py"
        ):

            module_name = file[:-3]

            module = importlib.import_module(
                f"app.agents.{module_name}"
            )

            AGENTS[
                module.NAME
            ] = {

                "handler":
                    module.execute,

                "capabilities":
                    module.CAPABILITIES
            }


load_agents()