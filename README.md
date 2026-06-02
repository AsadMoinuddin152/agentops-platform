# AgentOps Platform

## Overview

AgentOps Platform is a local-first Agentic AI runtime built using
Docker, FastAPI, Ollama, and local language models.

The platform evolved through multiple architecture phases to support:

-   Multi-agent execution
-   Dynamic skill plugins
-   Workflow orchestration
-   Local semantic RAG
-   Telemetry and observability
-   Plugin-ready architecture

This project focuses on building an extensible and observable AI runtime
that runs locally.

------------------------------------------------------------------------

## Tech Stack

### Backend

-   Python
-   FastAPI
-   Docker
-   Docker Compose
-   Ollama
-   Local Qwen Model

### AI + RAG

-   ChromaDB
-   Sentence Transformers
-   Local Embeddings
-   Semantic Retrieval

### Observability

-   JSONL Telemetry
-   Metrics Processing
-   Dashboard APIs

------------------------------------------------------------------------

## Architecture

Current runtime flow:

``` text
User
→ Orchestrator
→ Agent Router
→ Agent
→ Skill Router
→ Dynamic Skill Registry
→ Skill Executor
→ Skill Chain
→ Tools / RAG
→ Telemetry + Logs
```

------------------------------------------------------------------------

## Completed Phases

### Phase 1 --- Foundation

-   Docker setup
-   FastAPI runtime
-   Ollama integration
-   Tool layer
-   Memory
-   Swagger testing

### Phase 2 --- Multi-Agent Runtime

-   Multi-agent orchestrator
-   Coding Agent
-   Research Agent
-   Agent routing
-   ReAct-style tool use
-   Telemetry and observability

### Phase 3 --- Plugin + Workflow + Local RAG

-   Dynamic skill loading
-   Plugin architecture
-   Skill routing
-   Skill telemetry
-   Dependency chaining
-   Workflow execution
-   ChromaDB integration
-   Semantic retrieval
-   RAG skill integration

### Phase 4 --- Observability (In Progress)

-   Telemetry storage
-   Metrics APIs
-   Agent analytics
-   Skill analytics
-   Dashboard UI (planned)

------------------------------------------------------------------------

## Current Features

### Agents

-   Coding Agent
-   Research Agent
-   Metrics Agent

### Skills

-   Dynamic skill registry
-   Plugin-based skills
-   Dependency-aware execution
-   RAG integration

### Observability

-   Agent traces
-   Skill analytics
-   Tool usage tracking
-   Chain telemetry
-   Latency monitoring
-   LLM and RAG metrics

------------------------------------------------------------------------

## Run Locally

### Start containers

``` bash
docker compose up --build
```

### Open Swagger

``` text
http://localhost:8000/docs
```

### Dashboard

``` text
http://localhost:8000/dashboard
```

------------------------------------------------------------------------

## Roadmap

### Phase 4

Observability UI + Dashboard

### Phase 5

Advanced Multi-Agent Collaboration

### Phase 6

Distributed Agent Ecosystem

------------------------------------------------------------------------

## Project Goal

Build a local-first, observable, extensible Agentic AI platform with
multi-agent orchestration, semantic retrieval, and production-style
observability.
