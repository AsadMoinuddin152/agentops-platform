from app.core.config import MEMORY_LIMIT

memory_store = []


def save_memory(message):

    memory_store.append(message)

    if len(memory_store) > MEMORY_LIMIT:
        memory_store.pop(0)


def get_memory():

    return "\n".join(memory_store)