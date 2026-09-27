# 08 — Scalability

> *Scalability is not about handling 1 billion users. It is about not collapsing under 100.*

This section covers how systems grow — and why many fail before they reach production. You will learn the difference between vertical and horizontal scaling, how to identify bottlenecks, and the architectural patterns that allow systems to handle 10x, 100x, and 1000x growth. Each chapter also shows how the same ideas apply to AI inference, where requests vary a thousandfold in cost and GPUs are the scarce resource.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [Vertical vs Horizontal Scaling](Vertical-vs-Horizontal-Scaling.md) | ✅ Complete | 40 minutes |
| 2 | [How Load Balancing Works](How-Load-Balancing-Works.md) | ✅ Complete | 30 minutes |
| 3 | [Database Sharding](Database-Sharding.md) | ✅ Complete | 40 minutes |
| 4 | [Rate Limiting and Throttling](Rate-Limiting-and-Throttling.md) | ✅ Complete | 40 minutes |
| 5 | [Auto-scaling and Capacity Planning](Auto-scaling-and-Capacity-Planning.md) | ✅ Complete | 40 minutes |

## Key Ideas

- **Scalability is not a feature you add later**: It is an architectural property that must be designed from the start.
- **The bottleneck moves**: As you solve one bottleneck, another appears. Scaling is an ongoing process, not a one-time fix.
- **Horizontal scaling is harder but more powerful**: Adding more machines is more complex than buying a bigger machine, but it has no theoretical limit.
- **Meter work, not requests** *(AI era)*: For LLM workloads, rate limits, load balancing, and capacity plans must count tokens and cost, not request counts.

## Prerequisites

Distributed Systems (Section 05) recommended.
