# 05 — Distributed Systems

> *A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable.* — Leslie Lamport

This is the hardest section in the handbook — and the most important. Distributed systems power every major service you use: Google Search, Netflix, WhatsApp, Uber, Amazon. They also power every AI product: an LLM call is a slow, rate-limited, nondeterministic remote call, and an AI agent is a distributed workflow. Understanding why they are difficult is the mark of a senior engineer.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [Why Distributed Systems Are Hard](Why-Distributed-Systems-Are-Hard.md) | ✅ Complete | 45 minutes |
| 2 | [CAP Theorem Explained](CAP-Theorem-Explained.md) | ✅ Complete | 40 minutes |
| 3 | [Consistency vs Availability](Consistency-vs-Availability.md) | ✅ Complete | 45 minutes |
| 4 | How Large Systems Handle Failures | 📝 Planned | — |
| 5 | [How Caching Works](How-Caching-Works.md) | ✅ Complete | 45 minutes |
| 6 | Consensus Algorithms (Paxos, Raft) | 📝 Planned | — |
| 7 | Distributed Databases | 📝 Planned | — |
| 8 | Durable Execution and Long-Running Workflows | 📝 Planned | — |

## Key Ideas

- **The network is not reliable**: Messages get lost, delayed, or duplicated.
- **There is no global clock**: Two machines cannot agree on "right now."
- **Partial failure**: Some parts of the system may be failing while others work perfectly.
- **Distributed systems are about managing uncertainty**: You can't prevent failures, but you can design systems that survive them.
- **Success at the transport layer is not success** *(AI era)*: A model call can return HTTP 200 with wrong, malformed, or incomplete content — validate every response.
- **Agents need idempotency** *(AI era)*: Retried tool calls with side effects must not act twice.

## Prerequisites

Sections 01–04 recommended. Understanding of basic networking (Section 03) is especially helpful.
