# 14 — Learning Paths

> *The handbook is a map. These learning paths are the routes.*

This section provides guided reading paths for different roles and goals. Each path lists chapters in a suggested order. Chapters marked 📝 are planned; skip them for now and come back when they're published.

## Choose Your Path

| Path | For Whom | Est. Reading Time (published chapters) |
|------|----------|----------------------------------------|
| [The Beginner's Path](#the-beginners-path) | New engineers (0–2 years) | ~7 hours |
| [The AI-Era Essentials Path](#the-ai-era-essentials-path) | Every engineer using AI tools today | ~2–3 hours |
| [The AI Engineer Path](#the-ai-engineer-path) | Engineers building LLM-powered products | ~10 hours |
| [The Backend Path](#the-backend-path) | Backend engineers deepening their understanding | ~8–9 hours |
| [The System Design Path](#the-system-design-path) | Interview prep or designing at scale | ~7–8 hours |
| [The SRE / Production Path](#the-sre--production-path) | Engineers focused on reliability and operations | ~4–5 hours |
| [The Leadership Path](#the-leadership-path) | Senior engineers and tech leads | ~2–3 hours |
| **The Complete Journey** | Cover to cover, sections 01 → 15 | 20–25 hours |

---

## The Beginner's Path

*Goal: build an accurate mental model of how software, computers, and the internet actually work.*

1. [Why Software Exists](../01-Foundations/Why-Software-Exists.md)
2. [How To Think Like An Engineer](../01-Foundations/How-To-Think-Like-An-Engineer.md)
3. [How To Solve Problems Systematically](../01-Foundations/How-To-Solve-Problems-Systematically.md)
4. [What Happens When You Press A Key](../02-How-Computers-Work/What-Happens-When-You-Press-A-Key.md)
5. [How Memory Works](../02-How-Computers-Work/How-Memory-Works.md)
6. [How The Internet Really Works](../03-How-The-Internet-Works/How-The-Internet-Really-Works.md)
7. [How A Webpage Reaches Your Screen](../03-How-The-Internet-Works/How-A-Webpage-Reaches-Your-Screen.md)
8. [How Databases Work](../04-Data-And-Storage/How-Databases-Work.md)
9. [How Caching Works](../05-Distributed-Systems/How-Caching-Works.md)
10. [How LLMs Actually Work](../15-AI-Era-Engineering/How-LLMs-Actually-Work.md)
11. [Engineering With AI Assistants](../15-AI-Era-Engineering/Engineering-With-AI-Assistants.md)

**Beginner tip:** Use AI to *explain*, not to *skip*. After each chapter, close it and try to explain the core idea to an AI assistant in your own words, then ask it to point out gaps (see [Studying With an AI Assistant](#studying-with-an-ai-assistant) below).

---

## The AI-Era Essentials Path

*Goal: use AI tools effectively and safely, whatever your role. Short enough to finish in a week.*

1. [How To Think Like An Engineer](../01-Foundations/How-To-Think-Like-An-Engineer.md) — especially "It works" vs. "it's correct," and its *In the AI Era* section
2. [How LLMs Actually Work](../15-AI-Era-Engineering/How-LLMs-Actually-Work.md)
3. [Engineering With AI Assistants](../15-AI-Era-Engineering/Engineering-With-AI-Assistants.md)
4. [Securing AI Systems](../15-AI-Era-Engineering/Securing-AI-Systems.md) — at least the Core Concepts and Checklist
5. *In the AI Era* sections of: [How Operating Systems Work](../02-How-Computers-Work/How-Operating-Systems-Work.md) (sandboxing agents), [Backup, Recovery, and Durability](../04-Data-And-Storage/Backup-Recovery-and-Durability.md) (agents with write access), and [How HTTPS Protects Your Data](../03-How-The-Internet-Works/How-HTTPS-Protects-Your-Data.md) (API keys and data handling)

---

## The AI Engineer Path

*Goal: design, build, evaluate, secure, and operate products with LLMs inside them.*

**Part 1 — The model as a component**
1. [How LLMs Actually Work](../15-AI-Era-Engineering/How-LLMs-Actually-Work.md)
2. [The Memory Hierarchy](../02-How-Computers-Work/The-Memory-Hierarchy-Explained.md) and [How Memory Works](../02-How-Computers-Work/How-Memory-Works.md) — why context, KV cache, and model size behave as they do
3. [HTTP, TCP/IP, and the Protocol Stack](../03-How-The-Internet-Works/HTTP-TCP-IP-and-the-Protocol-Stack.md) — streaming and long-lived requests

**Part 2 — Building the system**
4. [Building LLM-Powered Systems](../15-AI-Era-Engineering/Building-LLM-Powered-Systems.md)
5. [How Databases Work](../04-Data-And-Storage/How-Databases-Work.md) and [SQL vs NoSQL](../04-Data-And-Storage/SQL-vs-NoSQL-The-Real-Difference.md) — vector search in context
6. [Data Replication Strategies](../04-Data-And-Storage/Data-Replication-Strategies.md) and [Consistency vs Availability](../05-Distributed-Systems/Consistency-vs-Availability.md) — keeping RAG indexes correct
7. [Why Distributed Systems Are Hard](../05-Distributed-Systems/Why-Distributed-Systems-Are-Hard.md) — agents as distributed workflows
8. [How Caching Works](../05-Distributed-Systems/How-Caching-Works.md) — prompt, response, and semantic caching

**Part 3 — Quality, safety, and scale**
9. [Evaluating AI Systems](../15-AI-Era-Engineering/Evaluating-AI-Systems.md)
10. [Securing AI Systems](../15-AI-Era-Engineering/Securing-AI-Systems.md)
11. [Rate Limiting and Throttling](../08-Scalability/Rate-Limiting-and-Throttling.md) and [How Load Balancing Works](../08-Scalability/How-Load-Balancing-Works.md)
12. [Auto-scaling and Capacity Planning](../08-Scalability/Auto-scaling-and-Capacity-Planning.md)
13. [Designing An AI Assistant Over Private Data](../06-System-Design/Designing-An-AI-Assistant-Over-Private-Data.md) and [Designing An AI Gateway](../06-System-Design/Designing-An-AI-Gateway.md) — two complete AI system designs
14. [Operating LLM Features: Cost, Latency, and Quality](../11-Production-Engineering/Operating-LLM-Features.md)

**Capstone project:** Build a question-answering assistant over a set of documents you know well (your team's docs, a product manual, this handbook). Include hybrid retrieval with citations, an eval set of at least 30 questions, a token budget per user, trace logging, and a written threat model using the lethal-trifecta test.

---

## The Backend Path

1. [How Operating Systems Work](../02-How-Computers-Work/How-Operating-Systems-Work.md)
2. [HTTP, TCP/IP, and the Protocol Stack](../03-How-The-Internet-Works/HTTP-TCP-IP-and-the-Protocol-Stack.md)
3. [How DNS Works](../03-How-The-Internet-Works/How-DNS-Works.md)
4. [How HTTPS Protects Your Data](../03-How-The-Internet-Works/How-HTTPS-Protects-Your-Data.md)
5. [How Databases Work](../04-Data-And-Storage/How-Databases-Work.md)
6. [SQL vs NoSQL: The Real Difference](../04-Data-And-Storage/SQL-vs-NoSQL-The-Real-Difference.md)
7. [Data Replication Strategies](../04-Data-And-Storage/Data-Replication-Strategies.md)
8. [Why Distributed Systems Are Hard](../05-Distributed-Systems/Why-Distributed-Systems-Are-Hard.md)
9. [How Caching Works](../05-Distributed-Systems/How-Caching-Works.md)
10. [Rate Limiting and Throttling](../08-Scalability/Rate-Limiting-and-Throttling.md)
11. [Database Sharding](../08-Scalability/Database-Sharding.md)
12. [Building LLM-Powered Systems](../15-AI-Era-Engineering/Building-LLM-Powered-Systems.md) — most backends now call a model somewhere
13. [The Most Common Web Attacks](../09-Security/The-Most-Common-Web-Attacks.md) — the bugs every backend engineer must prevent
14. [Cryptography for Engineers](../09-Security/Cryptography-For-Engineers.md)

---

## The System Design Path

1. [How To Think Like An Engineer](../01-Foundations/How-To-Think-Like-An-Engineer.md)
2. [Why Distributed Systems Are Hard](../05-Distributed-Systems/Why-Distributed-Systems-Are-Hard.md)
3. [CAP Theorem Explained](../05-Distributed-Systems/CAP-Theorem-Explained.md)
4. [Consistency vs Availability](../05-Distributed-Systems/Consistency-vs-Availability.md)
5. [How Caching Works](../05-Distributed-Systems/How-Caching-Works.md)
6. [Vertical vs Horizontal Scaling](../08-Scalability/Vertical-vs-Horizontal-Scaling.md)
7. [How Load Balancing Works](../08-Scalability/How-Load-Balancing-Works.md)
8. [Database Sharding](../08-Scalability/Database-Sharding.md)
9. [Rate Limiting and Throttling](../08-Scalability/Rate-Limiting-and-Throttling.md)
10. [Auto-scaling and Capacity Planning](../08-Scalability/Auto-scaling-and-Capacity-Planning.md)
11. [Building LLM-Powered Systems](../15-AI-Era-Engineering/Building-LLM-Powered-Systems.md) — "design an AI assistant" is now a common interview question
12. [How To Design Any System](../06-System-Design/How-To-Design-Any-System.md) — the method to use in every interview
13. [How To Handle 1 Million Users](../06-System-Design/How-To-Handle-1-Million-Users.md)
14. Practice designs: [Chat](../06-System-Design/Designing-A-Chat-System.md) · [Payments](../06-System-Design/Designing-A-Payment-System.md) · [Search](../06-System-Design/Designing-A-Search-System.md) · [AI Assistant](../06-System-Design/Designing-An-AI-Assistant-Over-Private-Data.md) · [AI Gateway](../06-System-Design/Designing-An-AI-Gateway.md)

**Interview tip:** Practice with an AI as your interviewer — ask it to play a skeptical senior engineer who pushes back on every tradeoff you state. Then write down the questions that stumped you and find the answers in the handbook, not in the AI's reply.

---

## The SRE / Production Path

1. [How Operating Systems Work](../02-How-Computers-Work/How-Operating-Systems-Work.md)
2. [Why Distributed Systems Are Hard](../05-Distributed-Systems/Why-Distributed-Systems-Are-Hard.md)
3. [Backup, Recovery, and Durability](../04-Data-And-Storage/Backup-Recovery-and-Durability.md)
4. [Rate Limiting and Throttling](../08-Scalability/Rate-Limiting-and-Throttling.md)
5. [Auto-scaling and Capacity Planning](../08-Scalability/Auto-scaling-and-Capacity-Planning.md)
6. [Evaluating AI Systems](../15-AI-Era-Engineering/Evaluating-AI-Systems.md) — quality as a production signal
7. [Securing AI Systems](../15-AI-Era-Engineering/Securing-AI-Systems.md) — especially "Securing Coding Agents"
8. [Why Systems Go Down](../10-Reliability/Why-Systems-Go-Down.md)
9. [How Google Handles Failures](../10-Reliability/How-Google-Handles-Failures.md) — SLOs and error budgets
10. [How Netflix Builds Resilient Systems](../10-Reliability/How-Netflix-Builds-Resilient-Systems.md)
11. [Observability: Monitoring, Alerting, and Debugging](../10-Reliability/Observability-Monitoring-Alerting-And-Debugging.md)
12. [Disaster Recovery Explained](../10-Reliability/Disaster-Recovery-Explained.md)
13. [Graceful Degradation for AI Features](../10-Reliability/Graceful-Degradation-For-AI-Features.md)
14. [The Life of a Production Request](../11-Production-Engineering/The-Life-Of-A-Production-Request.md)
15. [Deployments: Strategies and Risks](../11-Production-Engineering/Deployments-Strategies-And-Risks.md)
16. [Incident Response and Postmortems](../11-Production-Engineering/Incident-Response-And-Postmortems.md)
17. [SLOs in Practice](../11-Production-Engineering/SLOs-In-Practice.md)
18. [Capacity Planning in Practice](../11-Production-Engineering/Capacity-Planning-In-Practice.md)

---

## The Leadership Path

1. [How To Think Like An Engineer](../01-Foundations/How-To-Think-Like-An-Engineer.md)
2. [Why Software Exists](../01-Foundations/Why-Software-Exists.md)
3. [Engineering With AI Assistants](../15-AI-Era-Engineering/Engineering-With-AI-Assistants.md) — especially "Production Engineering Perspective" and the leadership interview questions
4. [Securing AI Systems](../15-AI-Era-Engineering/Securing-AI-Systems.md) — the organization-wide standards question
5. [Evaluating AI Systems](../15-AI-Era-Engineering/Evaluating-AI-Systems.md) — building an evaluation culture
6. 📝 Section 12 (Engineering Leadership)

---

## Studying With an AI Assistant

AI assistants can make you learn much faster — or give you the feeling of learning without the substance. The difference is whether *you* do the thinking. These prompts keep you in the driver's seat.

**1. Explain it back (after reading a chapter).**
```
I just read about <topic>. I'll explain it in my own words.
Don't correct me as I go. Afterward, tell me what I got wrong,
what I left out that matters most, and one question that would
expose whether I really understand it.
```

**2. Quiz me.**
```
Quiz me on <topic> one question at a time, starting easy and
getting harder. Wait for my answer before continuing. Include at
least one question about failure scenarios and one about tradeoffs.
```

**3. Stress-test a design.**
```
Here is my design for <system>. Act as a skeptical staff engineer.
Find the three most likely ways it fails in production and the
tradeoff I seem not to have considered. Don't propose a new design.
```

**4. Connect the concepts.**
```
How does <concept from chapter A> relate to <concept from chapter B>?
Give me a concrete scenario where both matter at once.
```

**5. Make it concrete.**
```
Give me a small hands-on experiment (under 30 minutes, on my laptop)
that would let me observe <concept> directly. Tell me what I should
expect to see, and what it would mean if I saw something different.
```

**Rules of thumb**
- Read the chapter first. Use the AI to *test* understanding, not replace reading.
- Treat the AI's explanations like any secondary source: verify claims that matter against the chapter's Further Reading.
- Run the experiments. Seeing a cache miss, a DNS lookup, or a race condition yourself teaches more than any explanation.
- Write your own notes. Summarizing in your own words is where most of the learning happens.
