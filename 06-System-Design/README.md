# 06 — System Design

> *System design is the art of making the right tradeoffs before writing a single line of code.*

This section teaches you how to design systems at any scale — from a single-server application to a global service handling billions of requests. The emphasis is on the *process* of design: gathering requirements, identifying constraints, evaluating tradeoffs, and making decisions. The same process applies when one of the components is an AI model.

## Chapters

| # | Chapter | Status |
|---|---------|--------|
| 1 | How To Design Any System | 📝 Planned |
| 2 | How To Handle 1 Million Users | 📝 Planned |
| 3 | Designing A Chat System | 📝 Planned |
| 4 | Designing A Payment System | 📝 Planned |
| 5 | Designing A Search System | 📝 Planned |
| 6 | Designing An AI Assistant Over Private Data (RAG + Tools) | 📝 Planned |
| 7 | Designing An AI Gateway: Routing, Quotas, and Fallbacks | 📝 Planned |

Until chapters 6–7 are written, see [Building LLM-Powered Systems](../15-AI-Era-Engineering/Building-LLM-Powered-Systems.md).

## Key Ideas

- **Start with requirements, not architecture**: The wrong system for the right requirements is still right. The right system for the wrong requirements is useless.
- **Constraints define the design**: A system for 100 users and a system for 100 million users are fundamentally different.
- **There are no perfect designs**: Every decision is a tradeoff. Good engineers articulate tradeoffs clearly.
- **Estimate in tokens, too** *(AI era)*: For AI features, back-of-the-envelope math includes tokens per request, cost per request, and time to first token.
- **Use the simplest AI pattern that works** *(AI era)*: A single prompt beats a workflow, which beats an agent — until the evidence says otherwise.

## Prerequisites

Distributed Systems (Section 05) recommended.
