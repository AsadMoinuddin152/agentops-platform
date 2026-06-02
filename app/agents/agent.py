from app.tools import TOOLS
from app.ollama_client import ask_llm
from app.memory import save_memory, get_memory


def run_agent(user_input):

    text = user_input.lower()

    save_memory(f"User: {user_input}")

    if "time" in text:

        result = TOOLS["time"]()

        save_memory(f"Agent: {result}")

        return f"[Tool: time]\n{result}"

    elif "list files" in text:

        result = TOOLS["list_files"]()

        save_memory(f"Agent: {result}")

        return f"[Tool: list_files]\n{result}"

    elif text.startswith("read file"):

        filename = user_input.replace("read file", "").strip()

        result = TOOLS["read_file"](filename)

        save_memory(f"Agent: file read")

        return f"[Tool: read_file]\n{result}"

    else:

        memory_context = get_memory()

        prompt = f"""
        You are a local AI super agent.

        Conversation Memory:
        {memory_context}

        User:
        {user_input}

        Think carefully and respond.
        """

        response = ask_llm(prompt)

        save_memory(f"Agent: {response}")

        return response