# 07 — Software Architecture

> *Architecture is about the important stuff. Whatever that is.* — Martin Fowler

This section covers the principles and patterns of software architecture — the high-level structure of software systems, the boundaries between components, and the decisions that are hardest to change. It also covers how to change architecture safely over time, and where AI components fit.

Start with **What Is Software Architecture?** — it defines architecture as decisions measured by cost of change, which every other chapter builds on.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [What Is Software Architecture?](What-Is-Software-Architecture.md) | ✅ Complete | 10 minutes |
| 2 | [Monoliths vs Microservices: The Real Tradeoffs](Monoliths-vs-Microservices-The-Real-Tradeoffs.md) | ✅ Complete | 10 minutes |
| 3 | [Coupling, Cohesion, and Boundaries](Coupling-Cohesion-And-Boundaries.md) | ✅ Complete | 10 minutes |
| 4 | [Event-Driven Architecture](Event-Driven-Architecture.md) | ✅ Complete | 10 minutes |
| 5 | [How To Refactor Large Systems](How-To-Refactor-Large-Systems.md) | ✅ Complete | 10 minutes |
| 6 | [Where the Model Fits: Architecting With AI Components](Where-The-Model-Fits-Architecting-With-AI-Components.md) | ✅ Complete | 10 minutes |

## Key Ideas

- **Architecture is about the hard-to-change decisions**: The database, the communication style, service boundaries, data ownership, public APIs. Get these right, and everything else is easier.
- **Quality attributes drive architecture**: Scalability, availability, security, and changeability — not features — decide between designs.
- **Coupling is the enemy**: The more components depend on each other, the harder the system is to change. Aim for high cohesion and low, explicit coupling.
- **Start with a modular monolith**: Microservices solve organizational scaling problems at the cost of distributed-systems complexity.
- **Architecture emerges and evolves**: Record decisions, enforce rules with fitness functions, and change systems incrementally rather than rewriting them.
- **Isolate the model behind an interface** *(AI era)*: Models and providers change quickly. Keep prompts, model choice, and provider SDKs behind a task-shaped boundary.
- **AI proposes, code decides** *(AI era)*: Keep decisions about money, access, and safety deterministic and auditable.

## Prerequisites

Foundations (Section 01) and System Design (Section 06) recommended.
