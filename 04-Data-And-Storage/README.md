# 04 — Data And Storage

> *At the bottom of every application is data. How you store, retrieve, and protect it determines everything.*

This section covers databases, file systems, replication, and the fundamental tradeoffs involved in persisting data. You will learn why there is no single "best database," and how engineers choose between SQL, NoSQL, and everything in between — including vector search, which now sits underneath most AI features.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [How Databases Work](How-Databases-Work.md) | ✅ Complete | 30 minutes |
| 2 | [SQL vs NoSQL: The Real Difference](SQL-vs-NoSQL-The-Real-Difference.md) | ✅ Complete | 30 minutes |
| 3 | [How File Systems Work](How-File-Systems-Work.md) | ✅ Complete | 35 minutes |
| 4 | [Data Replication Strategies](Data-Replication-Strategies.md) | ✅ Complete | 35 minutes |
| 5 | [Backup, Recovery, and Durability](Backup-Recovery-and-Durability.md) | ✅ Complete | 35 minutes |
| 6 | Vector Search and Embeddings | 📝 Planned | — |

## Key Ideas

- **Data is the most valuable asset in any system.** Everything else can be rebuilt; data cannot.
- **The storage hierarchy**: Hot data in memory, warm data on SSD, cold data on disk or tape.
- **Consistency models**: How "up to date" does your data need to be? The answer changes everything.
- **A RAG index is a replica** *(AI era)*: It inherits every replication problem — lag, deletes, permission changes, and divergence from the source of truth.
- **Agents with write access make backups urgent** *(AI era)*: Point-in-time recovery and environment separation are the safety net for automated mistakes.

## Prerequisites

Foundations (Section 01) recommended. No database expertise required.
