

import re
import time

from app.agents.registry import AGENTS
from app.tools.tool_registry import (
    TOOLS,
    get_tool_trace
)
from app.core.memory import save_memory
from app.core.response_formatter import (
    format_response
)
from app.core.telemetry import log_event
from app.core.metrics import log_metric


def find_best_agent(user_input):

    text = user_input.lower()

    scores = {}
    reasons = {}

    for agent_name, config in AGENTS.items():

        score = 0
        matched = []

        for capability in config["capabilities"]:
            pattern = rf"\b{re.escape(capability.lower())}\b"
            if re.search(pattern, text):
                score += 1
                matched.append(capability)

        scores[
            agent_name
        ] = score

        reasons[
            agent_name
        ] = matched

    best_agent = max(
        scores,
        key=scores.get
    )

    return (
        AGENTS[
            best_agent
        ]["handler"],
        best_agent,
        reasons[
            best_agent
        ],
        scores
    )


def orchestrate(user_input):

    start = time.time()

    save_memory(
        f"User: {user_input}"
    )

    text = user_input.lower()

    # -------------------
    # TOOL LAYER
    # -------------------

    if "time" in text:
        result = TOOLS["time"]()
        tools = get_tool_trace()
        latency = round((time.time() - start) * 1000, 2)
        log_metric(component="agent", event="agent_routing", data={"path": "tool_layer", "tool": "time", "orchestration_duration_ms": latency})
        log_event({"prompt": user_input, "selected_agent": "tool_layer", "selected_skill": None, "routing_reason": ["time"], "tools_used": tools, "latency_ms": latency})
        response = format_response("Tool Layer", "Get time", result)
        response["telemetry"] = {"selected_agent": "tool_layer", "routing_reason": ["time"], "selected_skill": None, "skill_reason": [], "skill_chain": [], "tools_used": tools, "latency_ms": latency}
        return response

    elif "list files" in text:
        result = TOOLS["list_files"]()
        tools = get_tool_trace()
        latency = round((time.time() - start) * 1000, 2)
        log_metric(component="agent", event="agent_routing", data={"path": "tool_layer", "tool": "list_files", "orchestration_duration_ms": latency})
        log_event({"prompt": user_input, "selected_agent": "tool_layer", "selected_skill": None, "routing_reason": ["list files"], "tools_used": tools, "latency_ms": latency})
        response = format_response("Tool Layer", "List files", result)
        response["telemetry"] = {"selected_agent": "tool_layer", "routing_reason": ["list files"], "selected_skill": None, "skill_reason": [], "skill_chain": [], "tools_used": tools, "latency_ms": latency}
        return response

    # -------------------
    # AGENT ROUTING
    # -------------------

    (
        agent_handler,
        agent_name,
        reasons,
        all_scores
    ) = find_best_agent(
        user_input
    )

    response = agent_handler(
        user_input
    )

    selected_skill = None
    skill_reason = []
    skill_chain = []

    if isinstance(
        response,
        dict
    ):

        metadata = response.get(
            "metadata",
            {}
        )

        selected_skill = metadata.get(
            "selected_skill"
        )

        skill_reason = metadata.get(
            "skill_reason",
            []
        )

        skill_chain = metadata.get(
            "skill_chain",
            []
        )

    tools = get_tool_trace()

    latency = round(
        (
            time.time()
            - start
        ) * 1000,
        2
    )

    log_metric(
        component="agent",
        event="agent_routing",
        data={
            "path": "agent",
            "selected_agent":
                agent_name,
            "all_agent_scores":
                all_scores,
            "routing_reason":
                reasons,
            "orchestration_duration_ms":
                latency
        }
    )

    # -------------------
    # LOG EVENT
    # -------------------

    log_event({

        "prompt":
            user_input,

        "selected_agent":
            agent_name,

        "selected_skill":
            selected_skill,

        "routing_reason":
            reasons,

        "skill_reason":
            skill_reason,

        "skill_chain":
            skill_chain,

        "tools_used":
            tools,

        "latency_ms":
            latency
    })

    # -------------------
    # RESPONSE TELEMETRY
    # -------------------
    response[
        "telemetry"
    ] = {

        "selected_agent":
            agent_name,

        "routing_reason":
            reasons,

        "selected_skill":
            selected_skill,

        "skill_reason":
            skill_reason,

        "skill_chain":
            skill_chain,

        "tools_used":
            tools,

        "latency_ms":
            latency
    }

    return response