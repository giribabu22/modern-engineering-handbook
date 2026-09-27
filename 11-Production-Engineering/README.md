# 11 — Production Engineering

> *Writing code is 10% of the job. Running it reliably in production is the other 90%.*

This section covers what happens after you deploy — monitoring, incident response, capacity planning, deployment strategies, and the operational practices that separate professional engineering teams from the rest. As AI makes writing code faster, this "other 90%" becomes an even larger share of the job.

## Chapters

| # | Chapter | Status |
|---|---------|--------|
| 1 | The Life of a Production Request | 📝 Planned |
| 2 | Deployments: Strategies and Risks | 📝 Planned |
| 3 | Incident Response and Postmortems | 📝 Planned |
| 4 | Capacity Planning | 📝 Planned |
| 5 | SLOs, SLIs, and Error Budgets | 📝 Planned |
| 6 | Operating LLM Features: Cost, Latency, and Quality | 📝 Planned |

## Key Ideas

- **Code in production is not the same as code in development**: The environment is unpredictable, data is real, and everything is slower.
- **Observability is not monitoring**: Monitoring tells you something is wrong. Observability lets you ask *why* it's wrong.
- **Every incident is a learning opportunity**: Blameless postmortems turn failures into improvements.
- **Prompts and model versions are deployments** *(AI era)*: Version them, test them against evals, roll them out gradually, and keep a rollback path.
- **Trace every AI interaction** *(AI era)*: Model, prompt version, retrieved context, tool calls, tokens, cost, and outcome — or you won't be able to answer "why did it say that?"

## Prerequisites

Reliability (Section 10) recommended.
