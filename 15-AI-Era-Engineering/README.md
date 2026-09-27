# 15 — AI-Era Engineering

> *AI changes how software is written and what software can do. It does not change the fundamentals — it raises the stakes on them.*

This section covers the engineering knowledge that the rise of large language models (LLMs) has made essential: how these models actually work, how to build reliable products on top of them, how to test and secure them, and how to work effectively alongside AI coding assistants.

The theme throughout is continuity. Tokens and context windows are a resource budget. Retrieval is a data pipeline. Agents are distributed workflows. Prompt injection is injection. Evals are test suites. If you have read the earlier sections, you already know most of what you need — this section shows you where it applies.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [How LLMs Actually Work](How-LLMs-Actually-Work.md) | ✅ Complete | 15 minutes |
| 2 | [Engineering With AI Assistants](Engineering-With-AI-Assistants.md) | ✅ Complete | 10 minutes |
| 3 | [Building LLM-Powered Systems: Retrieval, Tools, and Agents](Building-LLM-Powered-Systems.md) | ✅ Complete | 10 minutes |
| 4 | [Evaluating AI Systems](Evaluating-AI-Systems.md) | ✅ Complete | 10 minutes |
| 5 | [Securing AI Systems](Securing-AI-Systems.md) | ✅ Complete | 15 minutes |
| 6 | [Operating LLM Features: Cost, Latency, and Quality](../11-Production-Engineering/Operating-LLM-Features.md) *(in Section 11)* | ✅ Complete | 10 minutes |
| 7 | Self-Hosting Models: GPUs, Serving, and Quantization | 📝 Planned | — |
| 8 | Fine-Tuning: When and How | 📝 Planned | — |

## Key Ideas

- **Verification is the bottleneck.** AI makes producing code and text cheap; knowing whether it is correct is still expensive. Invest in whatever makes verification fast.
- **The model is one component.** Context, retrieval, tools, validation, evaluation, and operations decide product quality.
- **Nondeterminism changes testing.** Quality becomes a rate measured over datasets, not a single assertion.
- **Text is an attack surface.** Any content a model reads can act as an instruction; limit what a manipulated model can do.
- **Enforce guarantees in code.** Authorization, limits, and approvals belong outside the model.

## How This Section Connects to the Rest of the Handbook

| AI concept | Built on |
|-----------|---------|
| Context windows, KV cache, prompt caching | [Memory Hierarchy](../02-How-Computers-Work/The-Memory-Hierarchy-Explained.md), [Caching](../05-Distributed-Systems/How-Caching-Works.md) |
| Streaming responses, long-lived requests | [HTTP, TCP/IP, and the Protocol Stack](../03-How-The-Internet-Works/HTTP-TCP-IP-and-the-Protocol-Stack.md) |
| RAG indexes and freshness | [Data Replication](../04-Data-And-Storage/Data-Replication-Strategies.md), [Consistency vs Availability](../05-Distributed-Systems/Consistency-vs-Availability.md) |
| Agents, retries, idempotency | [Why Distributed Systems Are Hard](../05-Distributed-Systems/Why-Distributed-Systems-Are-Hard.md) |
| Token budgets and quotas | [Rate Limiting](../08-Scalability/Rate-Limiting-and-Throttling.md), [Capacity Planning](../08-Scalability/Auto-scaling-and-Capacity-Planning.md) |
| Sandboxed agents | [How Operating Systems Work](../02-How-Computers-Work/How-Operating-Systems-Work.md) |
| Verifying AI output | [How To Think Like An Engineer](../01-Foundations/How-To-Think-Like-An-Engineer.md) |

Every completed chapter elsewhere in the handbook also ends with an **"In the AI Era"** section connecting its topic to modern AI systems.

## Prerequisites

Foundations (Section 01) for everyone. For the systems chapters, Sections 03–05 and 08 are strongly recommended. No machine-learning background is required.
