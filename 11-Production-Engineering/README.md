# 11 — Production Engineering

> *Writing code is 10% of the job. Running it reliably in production is the other 90%.*

This section covers what happens after you deploy — the path every request takes, deployment strategies, incident response, capacity planning, SLOs, and the operational practices that separate professional engineering teams from the rest. As AI makes writing code faster, this "other 90%" becomes an even larger share of the job — and AI features themselves need operating.

Start with **The Life of a Production Request** — it maps the path that every other chapter in this section protects.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [The Life of a Production Request](The-Life-Of-A-Production-Request.md) | ✅ Complete | 15 minutes |
| 2 | [Deployments: Strategies and Risks](Deployments-Strategies-And-Risks.md) | ✅ Complete | 10 minutes |
| 3 | [Incident Response and Postmortems](Incident-Response-And-Postmortems.md) | ✅ Complete | 10 minutes |
| 4 | [Capacity Planning in Practice](Capacity-Planning-In-Practice.md) | ✅ Complete | 10 minutes |
| 5 | [SLOs in Practice: Choosing, Implementing, and Using Them](SLOs-In-Practice.md) | ✅ Complete | 10 minutes |
| 6 | [Operating LLM Features: Cost, Latency, and Quality](Operating-LLM-Features.md) | ✅ Complete | 10 minutes |

## Key Ideas

- **Code in production is not the same as code in development**: The environment is unpredictable, data is real, and everything is slower.
- **Every hop costs time and adds a way to fail**: Latency budgets and propagated deadlines keep the request path healthy.
- **Small, gradual, reversible changes**: Canaries, feature flags, and fast rollback turn most bad deploys into non-events.
- **Mitigate first, learn afterward**: Incidents end faster with clear roles; postmortems make the next one less likely.
- **Plan for peaks and failures**: Capacity must cover forecast peaks with a zone or region missing.
- **Observability is not monitoring**: Monitoring tells you something is wrong. Observability lets you ask *why* it's wrong.
- **Prompts and model versions are deployments** *(AI era)*: Version them, test them against evals, roll them out gradually, and keep a rollback path.
- **Operate AI on three dials** *(AI era)*: Cost, latency, and quality — measured for every call, per feature.

## Prerequisites

Reliability (Section 10) recommended. Scalability (Section 08) is helpful for the capacity chapter.
