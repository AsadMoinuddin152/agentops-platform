import os
import json
from app.core.config import METRICS_FILE

NAME = "metrics_skill"

CAPABILITIES = [
    "metrics",
    "telemetry",
    "logs",
    "performance"
]


def execute(
    user_input,
    context=None
):

    if not os.path.exists(METRICS_FILE):
        return {
            "skill": NAME,
            "result": "No metrics logged yet. Please invoke some LLM or RAG operations first."
        }

    try:
        metrics = []
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    metrics.append(json.loads(line))

        # Summarize last 15 metrics
        recent = metrics[-15:]
        llm_calls = [m for m in recent if m.get("event") == "llm_call"]
        rag_queries = [m for m in recent if m.get("event") == "rag_query"]

        summary = "System Telemetry & Performance Summary:\n\n"
        if llm_calls:
            durations = [m["data"].get("total_duration_ms", 0) for m in llm_calls]
            total_duration = sum(durations)
            avg_duration = round(total_duration / len(llm_calls), 2)
            total_tps = sum(m["data"].get("tokens_per_second", 0) for m in llm_calls)
            avg_tps = round(total_tps / len(llm_calls), 2)
            summary += f"- LLM Calls Logged: {len(llm_calls)}\n"
            summary += f"- Avg LLM Latency: {avg_duration} ms (Individual: {', '.join(f'{d} ms' for d in durations)})\n"
            summary += f"- Avg LLM Token Speed: {avg_tps} tokens/sec\n"
        else:
            summary += "- No recent LLM calls registered in metrics logs.\n"

        if rag_queries:
            rag_durations = [m["data"].get("retrieval_duration_ms", 0) for m in rag_queries]
            total_rag_duration = sum(rag_durations)
            avg_rag_duration = round(total_rag_duration / len(rag_queries), 2)
            summary += f"- RAG Queries Logged: {len(rag_queries)}\n"
            summary += f"- Avg Vector DB Retrieval Latency: {avg_rag_duration} ms (Individual: {', '.join(f'{d} ms' for d in rag_durations)})\n"
        else:
            summary += "- No recent RAG search activities logged.\n"

        return {
            "skill": NAME,
            "result": summary
        }

    except Exception as e:
        return {
            "skill": NAME,
            "result": f"Error parsing metrics file: {e}"
        }
