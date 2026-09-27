# 07 — Software Architecture

> *Architecture is about the important stuff. Whatever that is.* — Martin Fowler

This section covers the principles and patterns of software architecture — the high-level structure of software systems, the boundaries between components, and the decisions that are hardest to change.

## Chapters

| # | Chapter | Status |
|---|---------|--------|
| 1 | What Is Software Architecture? | 📝 Planned |
| 2 | Monoliths vs Microservices: The Real Tradeoffs | 📝 Planned |
| 3 | Coupling, Cohesion, and Boundaries | 📝 Planned |
| 4 | Event-Driven Architecture | 📝 Planned |
| 5 | How To Refactor Large Systems | 📝 Planned |
| 6 | Where the Model Fits: Architecting With AI Components | 📝 Planned |

## Key Ideas

- **Architecture is about the hard-to-change decisions**: The database, the programming language, the communication protocol between services. Get these right, and everything else is easier.
- **Coupling is the enemy**: The more components depend on each other, the harder the system is to change.
- **Architecture emerges**: The best architectures are not designed upfront — they evolve as understanding deepens.
- **Isolate the model behind an interface** *(AI era)*: Models and providers change quickly. Keep prompts, model choice, and provider SDKs behind a boundary so you can swap them without rewriting the application.
- **Clear boundaries help AI assistants too** *(AI era)*: Well-structured, consistent codebases with explicit interfaces are easier for both humans and coding agents to change safely.

## Prerequisites

Foundations (Section 01) and System Design (Section 06) recommended.
