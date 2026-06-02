import os
import importlib


SKILLS = {}


def load_skills():

    skills_dir = "app/skills"

    for file in os.listdir(
        skills_dir
    ):

        if (
            file.endswith(
                "_skill.py"
            )
            and file != "__init__.py"
        ):

            module_name = file[:-3]

            module = importlib.import_module(
                f"app.skills.{module_name}"
            )

            SKILLS[
                module.NAME
            ] = {

                "handler":
                    module.execute,

                "capabilities":
                    module.CAPABILITIES,

                "dependencies":
                    getattr(
                        module,
                        "DEPENDENCIES",
                        []
                    )
            }


load_skills()