# 06 — System Design

> *System design is the art of making the right tradeoffs before writing a single line of code.*

This section teaches you how to design systems at any scale — from a single-server application to a global service handling billions of requests. The emphasis is on the *process* of design: gathering requirements, identifying constraints, evaluating tradeoffs, and making decisions. The same process applies when one of the components is an AI model.

Start with **How To Design Any System** — it introduces the seven-step method every other chapter in this section applies to a real problem.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [How To Design Any System](How-To-Design-Any-System.md) | ✅ Complete | 20 minutes |
| 2 | [How To Handle 1 Million Users](How-To-Handle-1-Million-Users.md) | ✅ Complete | 15 minutes |
| 3 | [Designing A Chat System](Designing-A-Chat-System.md) | ✅ Complete | 15 minutes |
| 4 | [Designing A Payment System](Designing-A-Payment-System.md) | ✅ Complete | 15 minutes |
| 5 | [Designing A Search System](Designing-A-Search-System.md) | ✅ Complete | 15 minutes |
| 6 | [Designing An AI Assistant Over Private Data](Designing-An-AI-Assistant-Over-Private-Data.md) | ✅ Complete | 15 minutes |
| 7 | [Designing An AI Gateway: Routing, Quotas, and Fallbacks](Designing-An-AI-Gateway.md) | ✅ Complete | 15 minutes |

## Key Ideas

- **Start with requirements, not architecture**: The wrong system for the right requirements is still right. The right system for the wrong requirements is useless.
- **Constraints define the design**: A system for 100 users and a system for 100 million users are fundamentally different.
- **Estimate before you choose**: Back-of-the-envelope numbers turn opinions into constraints.
- **Find the hard part**: Most of a design's value is in two or three deep dives — ordering for chat, exactly-once charging for payments, ranking for search, permissions for AI assistants.
- **There are no perfect designs**: Every decision is a tradeoff. Good engineers articulate tradeoffs clearly.
- **Estimate in tokens, too** *(AI era)*: For AI features, back-of-the-envelope math includes tokens per request, cost per request, and time to first token.
- **Use the simplest AI pattern that works** *(AI era)*: A single prompt beats a workflow, which beats an agent — until the evidence says otherwise.

## Prerequisites

Distributed Systems (Section 05) recommended. Scalability (Section 08) is helpful for the later chapters.
