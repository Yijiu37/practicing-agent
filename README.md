# Practicing Agent

> An Agent that learns from its own execution experience and progressively improves its future behavior.

Practicing Agent is an experimental Agent framework focused on **learning from execution experience**.

Instead of treating an Agent run as an isolated process, the system records execution trajectories, evaluates outcomes, reflects on failures, and gradually turns useful experience into reusable behavioral knowledge.

## Core Idea

```text
Practice
   ↓
Execution
   ↓
Trajectory
   ↓
Evaluation
   ↓
Reflection
   ↓
Experience
   ↓
Improvement
   ↓
Better Practice
   ↺
```

The central idea is simple:

> **Experience should change how the Agent behaves in future executions.**

## Current Architecture

```text
User Task
    ↓
┌──────────────┐
│   LLM Node   │
└──────┬───────┘
       │
       ├── Final Answer
       │
       └── Tool Call
              ↓
       ┌──────────────┐
       │  Tool Node   │
       └──────┬───────┘
              │
              ↓
        Tool Result/Error
              │
              ↓
          LLM Node
              ↺
```

The current runtime implements a minimal graph-based Agent loop with:

* LLM reasoning
* Tool Calling
* Multiple tool execution
* Tool error handling
* Execution trajectory recording
* Evaluation
* Explicit Agent state
* A lightweight graph runtime

## Project Structure

```text
practicing-agent/
├── app/
│   ├── state.py
│   ├── trajectory.py
│   ├── evaluation.py
│   │
│   ├── tools/
│   │   ├── calculator.py
│   │   ├── user.py
│   │   └── registry.py
│   │
│   ├── nodes/
│   │   ├── llm.py
│   │   └── tool.py
│   │
│   ├── graph/
│   │   └── mini_graph.py
│   │
│   └── agent.py
│
├── tests/
├── main.py
├── requirements.txt
├── README.md
└── .env
```

## Design Principles

### 1. Execution is observable

Every Agent execution produces a trajectory describing what happened during the run.

### 2. Evaluation is separate from execution

The Agent runtime executes the task, while the evaluation layer determines how the execution performed.

### 3. Experience is different from state

`AgentState` represents the state of the current run.

`Experience` is intended to represent reusable knowledge that can survive across runs.

### 4. Learning should affect future behavior

The long-term goal is not simply to generate `SKILL.md` files from trajectories.

Instead:

```text
Experience
    ↓
Behavioral Improvement
    ↓
Future Execution
```

## Roadmap

* [x] Minimal LLM Agent
* [x] Tool Calling
* [x] Agent Loop
* [x] Multiple Tools
* [x] Tool Error Handling
* [x] Trajectory Recording
* [x] Basic Evaluation
* [ ] Reflection
* [ ] Experience Representation
* [ ] Persistent Experience Memory
* [ ] Experience Retrieval
* [ ] Experience-guided Execution
* [ ] Verified Behavioral Improvement
* [ ] RAG
* [ ] LangChain Integration
* [ ] LangGraph Integration
* [ ] MCP / Skills
* [ ] Agent Harness
* [ ] Evaluation & Observability
* [ ] FastAPI Backend
* [ ] Web UI

## Philosophy

Practicing Agent explores a simple question:

> **What if an Agent could treat every execution as practice?**

A successful execution provides evidence of useful behavior.

A failed execution provides information about what should change.

The system therefore aims to build a continuous loop:

```text
Experience → Reflection → Improvement → Practice
```

rather than treating each Agent run as an isolated interaction.

## Status

**Early-stage research / engineering project.**

The architecture is intentionally implemented from scratch before introducing higher-level Agent frameworks. This makes the underlying mechanisms explicit and provides a foundation for later integration with frameworks such as LangGraph.

## License

MIT
