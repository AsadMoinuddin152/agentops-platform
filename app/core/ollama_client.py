import requests
from app.core.config import OLLAMA_URL, MODEL
from app.core.metrics import log_metric


def ask_llm(prompt):

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    # Capture and log LLM metrics from Ollama response
    log_metric(
        component="llm",
        event="llm_call",
        data={
            "model":
                data.get("model", MODEL),
            "prompt_tokens":
                data.get("prompt_eval_count", 0),
            "output_tokens":
                data.get("eval_count", 0),
            "total_tokens":
                data.get("prompt_eval_count", 0)
                + data.get("eval_count", 0),
            "prompt_eval_duration_ms":
                round(
                    data.get("prompt_eval_duration", 0)
                    / 1_000_000,
                    2
                ),
            "eval_duration_ms":
                round(
                    data.get("eval_duration", 0)
                    / 1_000_000,
                    2
                ),
            "total_duration_ms":
                round(
                    data.get("total_duration", 0)
                    / 1_000_000,
                    2
                ),
            "load_duration_ms":
                round(
                    data.get("load_duration", 0)
                    / 1_000_000,
                    2
                ),
            "tokens_per_second":
                round(
                    data.get("eval_count", 0)
                    / max(
                        data.get("eval_duration", 1)
                        / 1_000_000_000,
                        0.001
                    ),
                    2
                )
        }
    )

    return data["response"]