import json
import os
import math
from app.agents.registry import AGENTS
from app.skills.registry import SKILLS
from app.core.config import LOG_FILE, METRICS_FILE


def load_jsonl(filepath):

    if not os.path.exists(filepath):
        return []

    records = []

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                if line.strip():

                    records.append(
                        json.loads(line)
                    )

    except Exception as e:

        print(
            f"Error reading {filepath}: {e}"
        )

    return records


def calculate_p95(values):

    if not values:
        return 0.0

    sorted_vals = sorted(values)

    idx = math.ceil(
        len(sorted_vals) * 0.95
    ) - 1

    return round(
        sorted_vals[
            max(0, idx)
        ],
        2
    )


# -------------------------------------------------------
# STATS (UNCHANGED)
# -------------------------------------------------------

def get_observability_stats():

    agent_logs = load_jsonl(
        LOG_FILE
    )

    metrics_logs = load_jsonl(
        METRICS_FILE
    )

    total_runs = len(
        agent_logs
    )

    latencies = [

        log.get(
            "latency_ms",
            0
        )

        for log in agent_logs

        if "latency_ms" in log
    ]

    avg_latency = round(
        sum(latencies)
        / len(latencies),
        2
    ) if latencies else 0.0

    p95_latency = calculate_p95(
        latencies
    )

    llm_calls = [

        m

        for m in metrics_logs

        if m.get(
            "event"
        ) == "llm_call"
    ]

    llm_latencies = [

        m["data"].get(
            "total_duration_ms",
            0
        )

        for m in llm_calls
    ]

    avg_llm_latency = round(
        sum(llm_latencies)
        / len(llm_calls),
        2
    ) if llm_calls else 0.0

    avg_tps = round(
        sum(
            m["data"].get(
                "tokens_per_second",
                0
            )
            for m in llm_calls
        )
        / len(llm_calls),
        2
    ) if llm_calls else 0.0

    rag_queries = [

        m

        for m in metrics_logs

        if m.get(
            "event"
        ) == "rag_query"
    ]

    rag_latencies = [

        m["data"].get(
            "retrieval_duration_ms",
            0
        )

        for m in rag_queries
    ]

    avg_rag_latency = round(
        sum(rag_latencies)
        / len(rag_queries),
        2
    ) if rag_queries else 0.0

    avg_hits = round(
        sum(
            m["data"].get(
                "vector_hits",
                0
            )
            for m in rag_queries
        )
        / len(rag_queries),
        2
    ) if rag_queries else 0.0

    return {
        "total_runs":
            total_runs,

        "avg_orchestration_latency_ms":
            avg_latency,

        "p95_orchestration_latency_ms":
            p95_latency,

        "llm_stats": {
            "total_calls":
                len(llm_calls),

            "avg_latency_ms":
                avg_llm_latency,

            "avg_tokens_per_sec":
                avg_tps
        },

        "rag_stats": {
            "total_queries":
                len(rag_queries),

            "avg_retrieval_ms":
                avg_rag_latency,

            "avg_hits":
                avg_hits
        }
    }


# -------------------------------------------------------
# AGENTS
# count + skills used
# -------------------------------------------------------

def get_agent_metrics():

    logs = load_jsonl(
        LOG_FILE
    )

    agents = {}

    # preload ALL agents dynamically

    for agent_name in AGENTS.keys():

        agents[
            agent_name
        ] = {

            "agent":
                agent_name,

            "calls":
                0,

            "skills":
                {}
        }

    # include tool layer if present

    agents.setdefault(
        "tool_layer",
        {
            "agent":
                "tool_layer",

            "calls":
                0,

            "skills":
                {}
        }
    )

    # aggregate logs

    for log in logs:

        agent = log.get(
            "selected_agent",
            "unknown"
        )

        skill = log.get(
            "selected_skill"
        )

        if agent not in agents:

            agents[
                agent
            ] = {

                "agent":
                    agent,

                "calls":
                    0,

                "skills":
                    {}
            }

        data = agents[
            agent
        ]

        data[
            "calls"
        ] += 1

        if skill:

            skills = data[
                "skills"
            ]

            skills[
                skill
            ] = skills.get(
                skill,
                0
            ) + 1

    return list(
        agents.values()
    )
    
# -------------------------------------------------------
# SKILLS
# count + called_by + tools
# -------------------------------------------------------

def get_skill_metrics():

    logs = load_jsonl(
        LOG_FILE
    )

    skills = {}

    # preload ALL skills dynamically

    for skill_name in SKILLS.keys():

        skills[
            skill_name
        ] = {

            "skill":
                skill_name,

            "calls":
                0,

            "called_by":
                {},

            "tools":
                {}
        }

    # aggregate logs

    for log in logs:

        skill = log.get(
            "selected_skill"
        )

        if not skill:
            continue

        agent = log.get(
            "selected_agent",
            "unknown"
        )

        tools = log.get(
            "tools_used",
            []
        )

        if skill not in skills:

            skills[
                skill
            ] = {

                "skill":
                    skill,

                "calls":
                    0,

                "called_by":
                    {},

                "tools":
                    {}
            }

        data = skills[
            skill
        ]

        data[
            "calls"
        ] += 1

        callers = data[
            "called_by"
        ]

        callers[
            agent
        ] = callers.get(
            agent,
            0
        ) + 1

        tool_map = data[
            "tools"
        ]

        for tool in tools:

            tool_map[
                tool
            ] = tool_map.get(
                tool,
                0
            ) + 1

    return list(
        skills.values()
    )
# -------------------------------------------------------
# CHAINS (UNCHANGED)
# -------------------------------------------------------

def get_chain_metrics():

    logs = load_jsonl(
        LOG_FILE
    )

    distribution = {}

    for log in logs:

        chain = log.get(
            "skill_chain",
            []
        )

        if chain:

            chain_str = (
                " -> ".join(
                    chain
                )
            )

            distribution[
                chain_str
            ] = distribution.get(
                chain_str,
                0
            ) + 1

    return distribution


# -------------------------------------------------------
# RECENT TRACES (UNCHANGED)
# -------------------------------------------------------

def get_recent_traces(
    limit=50
):

    logs = load_jsonl(
        LOG_FILE
    )

    return list(
        reversed(
            logs[-limit:]
        )
    )