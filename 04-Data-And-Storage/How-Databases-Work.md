# How Databases Work

*Underneath every "SELECT * FROM users" is a machine that has spent fifty years learning how to lie to you efficiently — pretending your data is safe, instantly available, and perfectly consistent, all at once.*

---

## Introduction

Imagine a librarian who never forgets where a single book is, can find any book among ten million in under a millisecond, will never lose a book even if the building catches fire mid-shelving, and can let a thousand people check out and return books simultaneously without ever handing the same book to two people at once. That librarian is impossible for a human. It is not impossible for a database.

A **database** is software engineered to solve one deceptively simple problem: store data durably, retrieve it quickly, and let many people change it at once without corrupting it. Every part of that sentence — "durably," "quickly," "many people," "without corrupting" — is a separate, hard engineering problem, and a modern database (PostgreSQL, MySQL, SQLite, Oracle, CockroachDB) is really four systems wearing a trench coat: a storage engine, a query engine, a transaction manager, and a recovery system.

Most engineers use databases every day and treat them as a black box: you write SQL, data comes back. That's fine for building CRUD apps. But when a query that used to take 5ms starts taking 5 seconds, when a "successful" write vanishes after a crash, or when two concurrent updates silently clobber each other, the black box stops being acceptable. You need to know what's inside it.

### Why Should Engineers Care

- **Performance debugging is impossible without internals.** You cannot reason about why an index helped (or didn't) without understanding B-trees.
- **Data loss is a career-ending bug.** Understanding write-ahead logging is the difference between "we lost 3 seconds of writes" and "we lost the whole database."
- **Every senior engineering interview touches this.** "How does an index work?" and "Explain ACID" are two of the most common systems questions asked at every level from mid to staff.
- **Choosing the right database requires knowing what's under the hood.** LSM-tree-based stores (Cassandra, RocksDB) and B-tree-based stores (PostgreSQL, MySQL/InnoDB) behave very differently under write-heavy workloads.
- **You will eventually build something like one.** Search indexes, event stores, and caching layers all borrow database internals.

### Where Is This Used

| Context | Example | Why It Matters |
|---|---|---|
| Web application backend | PostgreSQL storing user accounts | Correctness under concurrent signups |
| Financial systems | Oracle/PostgreSQL storing ledgers | ACID transactions prevent double-spending |
| Analytics | ClickHouse, Snowflake (columnar) | Column storage makes aggregate queries fast |
| Mobile apps | SQLite embedded database | Single-file durable storage on a phone |
| Distributed SaaS | CockroachDB, Spanner | Replicated, globally consistent transactions |
| Caching/session stores | Redis (in-memory, log-structured) | Speed over durability tradeoffs |
| Search | Elasticsearch (Lucene, LSM-based) | Optimized for write-heavy, full-text queries |

---

## The Problem It Solves

A database exists to answer a question that sounds trivial and isn't: **how do you let a program store more data than fits in memory, retrieve any piece of it in milliseconds, survive power loss without losing committed data, and let hundreds of clients read and write concurrently without seeing each other's half-finished work?**

Naively, you could just write data to a file. That works until:

1. The file gets larger than RAM, and reading any single record means scanning gigabytes.
2. Two processes write to the file at the same time and corrupt it.
3. The power goes out mid-write and the file is left in an unknown, half-written state.
4. You need to find "all users signed up in the last 7 days" and a full scan takes ten minutes.

Databases exist to solve exactly these four problems, respectively, with: **indexes**, **concurrency control (locks/MVCC)**, **write-ahead logging and crash recovery**, and **query optimization**.

### What Happens Without This?

Teams that try to roll their own persistence layer (flat files, ad-hoc JSON blobs, homegrown "databases") consistently rediscover the same failure modes that real databases solved decades ago:

- **Torn writes**: a crash during a multi-field update leaves some fields updated and others not, because there was no atomicity boundary.
- **Lost updates**: two threads read a value, both increment it, both write back — one increment is silently lost because there was no locking or MVCC.
- **O(n) lookups**: without an index, "find the user by email" degrades linearly as the dataset grows, and a system that was fast at 10,000 rows grinds to a halt at 10,000,000.
- **Unrecoverable corruption**: a machine loses power while a file is half-written, and there is no log to replay to figure out what state the file should be in.
- **No isolation**: a report-generation query reads data that is being modified mid-read, producing numbers that never existed at any single point in time.

This is why "just write it to a file" almost always eventually becomes "we accidentally rebuilt a worse, buggier database." Understanding the real thing is cheaper than reinventing it badly.

---

## Historical Background

- **1960s — Navigational databases.** IBM's **IMS** (Information Management System, 1966), built for the Apollo program, organized data as a hierarchy that programs had to navigate pointer-by-pointer. Charles Bachman's **IDS** (Integrated Data Store, 1964) introduced the network model. Both required application code to know the physical layout of data — brittle and hard to change.

- **1970 — The relational model.** **Edgar F. "Ted" Codd**, a mathematician at IBM's San Jose research lab, published *"A Relational Model of Data for Large Shared Data Banks"* in *Communications of the ACM*. Codd proposed representing data as simple tables (relations) and manipulating it with relational algebra, freeing applications from knowing physical storage details. This is arguably the single most influential paper in the history of data management.

- **1974 — SQL is born.** Donald Chamberlin and Raymond Boyce at IBM designed **SEQUEL** (Structured English Query Language, later renamed SQL) as a human-readable way to express Codd's relational algebra.

- **1979 — Oracle v2** becomes the first commercially available SQL relational database, released by Relational Software Inc. (later Oracle Corporation), founded by Larry Ellison, Bob Miner, and Ed Oates.

- **1979 — INGRES**, developed at UC Berkeley by Michael Stonebraker and Eugene Wong, becomes an influential academic RDBMS and the ancestor of Sybase, Microsoft SQL Server, and eventually PostgreSQL.

- **1986 — SQL becomes an ANSI standard**, and later an ISO standard (1987), cementing it as the lingua franca of databases.

- **1989 — POSTGRES** (Stonebraker again, Berkeley) is released, explicitly designed to extend the relational model with user-defined types and objects — it evolves into today's **PostgreSQL** (renamed 1996 when SQL support was added).

- **1995 — MySQL** is released by Michael Widenius and David Axmark, prioritizing speed and simplicity, and becomes the default database of the web (the "M" in the LAMP stack).

- **1996 — Berkeley DB** popularizes the embedded key-value store pattern that later influences LevelDB, RocksDB, and LSM-tree-based engines.

- **2006 — Google's Bigtable paper** describes a distributed storage system built on the **SSTable** and **LSM-tree** ideas (originally formalized by Patrick O'Neil et al. in the 1996 paper *"The Log-Structured Merge-Tree (LSM-Tree)"*), optimized for write-heavy workloads at massive scale.

- **2007 — Amazon's Dynamo paper** popularizes leaderless, eventually-consistent key-value storage, inspiring Cassandra, Riak, and Voldemort.

- **2011 — Google Spanner** demonstrates that globally distributed systems could still offer strong (externally consistent) transactional guarantees, using synchronized atomic clocks (TrueTime).

- **2010s–present — NewSQL and multi-model convergence.** CockroachDB, YugabyteDB, and TiDB combine relational SQL semantics with horizontally-scalable, replicated storage engines — closing the gap between "SQL" and "scales like NoSQL."

---

## Core Concepts

### 1. The Storage Engine

The storage engine is the part of the database that decides *how bytes are physically arranged on disk*. Two dominant families exist:

**B-Trees (and B+Trees)** — used by PostgreSQL, MySQL/InnoDB, SQLite, Oracle, SQL Server. Data is kept sorted in a balanced tree of fixed-size pages (commonly 4KB–16KB), updated in place.

```
                [ 50 | 100 ]
               /     |      \
        [10|30]   [60|80]   [110|150]
        /  |  \    /  |  \    /   |   \
     leaf leaf leaf ...              leaf pages
     (actual rows / row pointers live here)
```

- Reads: O(log n) page lookups — typically 3-4 levels deep even for billions of rows.
- Writes: update pages in place, which can cause random disk I/O (mitigated by the buffer pool cache and WAL, discussed below).

**LSM-Trees (Log-Structured Merge-Trees)** — used by Cassandra, RocksDB, LevelDB, HBase, and as an option in MongoDB (WiredTiger). Writes go to an in-memory sorted structure (a **memtable**), which is periodically flushed to disk as an immutable, sorted file (an **SSTable**). Background **compaction** merges SSTables over time.

```
Write path:
  write -> memtable (in RAM, sorted) -> flush -> SSTable_1 (disk)
                                                -> SSTable_2 (disk)
                                                -> SSTable_3 (disk)
  Background compaction merges SSTable_1..3 -> SSTable_merged (removes deleted/overwritten keys)
```

- Writes: always sequential (append-only) — extremely fast, ideal for write-heavy workloads.
- Reads: may need to check the memtable and multiple SSTables (mitigated with **Bloom filters** to skip files that definitely don't contain a key).

| Property | B-Tree | LSM-Tree |
|---|---|---|
| Write pattern | In-place, random I/O | Append-only, sequential I/O |
| Write throughput | Moderate | High |
| Read latency | Consistently low | Can require checking multiple files |
| Space amplification | Lower | Higher (until compaction) |
| Write amplification | Lower | Higher (due to compaction rewrites) |
| Best for | Read-heavy, balanced workloads | Write-heavy workloads (logs, time series) |
| Examples | PostgreSQL, InnoDB, SQLite | Cassandra, RocksDB, LevelDB, HBase |

### 2. Pages, the Buffer Pool, and Disk I/O

Databases don't read individual rows from disk — they read fixed-size **pages** (blocks), typically 4KB–16KB, because disks are efficient at reading contiguous blocks and inefficient at reading scattered single bytes. A **buffer pool** (a.k.a. page cache) keeps hot pages in RAM so repeated access avoids disk I/O entirely. Most of PostgreSQL and MySQL's performance tuning knobs (`shared_buffers`, `innodb_buffer_pool_size`) exist to control how much RAM this cache gets.

### 3. Indexes

An index is a secondary data structure — typically a B-tree — that maps a column's values to the physical location of the rows containing them, so the database doesn't need to scan every row to find a match.

```
Table (heap, unordered):
  row 1: id=88, email=carol@x.com
  row 2: id=12, email=alice@x.com
  row 3: id=45, email=bob@x.com

Index on email (B-tree, sorted):
  alice@x.com -> row 2
  bob@x.com   -> row 3
  carol@x.com -> row 1
```

Without the index: `WHERE email = 'bob@x.com'` requires scanning every row — O(n).
With the index: the B-tree lookup is O(log n), then one jump to the row.

**The cost is real**: every index must be updated on every INSERT, UPDATE, and DELETE that touches the indexed column. Tables with many indexes have slower writes — this is why "just add an index" is not a free lunch. Over-indexing a write-heavy table is one of the most common production performance mistakes.

### 4. Query Execution Pipeline

A SQL query does not execute as written. It travels through a pipeline:

```
SQL text
   |
   v
[ Parser ]        -> validates syntax, builds an Abstract Syntax Tree (AST)
   |
   v
[ Analyzer/Binder]-> resolves table/column names against the catalog, checks types
   |
   v
[ Query Planner/  -> generates multiple possible execution plans
  Optimizer ]         (e.g., index scan vs sequential scan vs hash join vs nested loop)
   |                  and picks the cheapest one using cost estimates and statistics
   v
[ Executor ]      -> runs the chosen plan, pulling rows page by page,
   |                  applying filters, joins, sorts, aggregates
   v
Result set
```

The **query optimizer** is the most sophisticated part of a database. It uses table statistics (row counts, value distributions, histograms) to estimate the *cost* of different plans — e.g., "should this join scan the small table first, or use the index on the large table?" — and picks the plan it estimates will be cheapest. This is why `EXPLAIN ANALYZE` is the single most useful debugging tool in SQL performance work: it shows you exactly what plan was chosen and why it might be wrong (usually because statistics are stale).

### 5. Transactions and ACID

A **transaction** is a group of operations that must succeed or fail as a single unit. ACID describes the guarantees:

| Guarantee | Meaning | What breaks without it |
|---|---|---|
| **Atomicity** | All operations in a transaction happen, or none do | Partial updates (e.g., money debited but not credited) |
| **Consistency** | The database moves from one valid state to another, respecting constraints | Foreign key violations, broken invariants |
| **Isolation** | Concurrent transactions don't see each other's uncommitted changes | Dirty reads, lost updates, phantom reads |
| **Durability** | Once committed, data survives crashes | "Successful" writes vanish after a power loss |

Isolation is implemented via **locking** (two-phase locking: acquire locks, release them only at commit) or **MVCC** (Multi-Version Concurrency Control: readers see a consistent snapshot of the data as of when their transaction started, while writers create new row versions rather than overwriting in place). PostgreSQL, Oracle, and MySQL/InnoDB all use MVCC by default, which is why readers in these databases generally don't block writers.

### 6. The Write-Ahead Log (WAL)

The WAL is the mechanism that makes durability and crash recovery possible. Before any change is applied to the actual data pages, it is first written — sequentially, which is fast — to an append-only log file. Only after the log record is safely on disk does the database consider the transaction committed.

```
Client: COMMIT
   |
   v
[ WAL: append "txn 501: UPDATE accounts SET balance=... WHERE id=7" ]
   |
   v
fsync() -- log record physically flushed to disk
   |
   v
Return "commit successful" to client
   |
   v
(later, asynchronously) actual data pages updated in the buffer pool / flushed to disk
```

If the machine crashes after the WAL record is fsynced but before the data page is updated, **recovery replays the WAL** on restart to bring the data pages up to date. This is why a database can promise durability without having to synchronously write every dirty page to disk on every commit — it only needs to guarantee the *log* is durable, and the log write is sequential (fast), while data page writes can happen lazily in the background.

---

## Real-World Analogy

Think of a database as a hospital's medical records department.

- The **storage engine** is the filing system itself — whether records are filed alphabetically in cabinets you update in place (B-tree) or new records are always added to the top of a stack, with an occasional weekend spent reorganizing the stack into an alphabetized master file (LSM-tree).
- **Indexes** are the card catalog by patient name, by doctor, by diagnosis code — you don't walk every cabinet aisle by aisle; you look up the card, which tells you exactly which cabinet and folder to go to.
- **The buffer pool** is the small stack of frequently requested charts kept on the front desk instead of the archive room — the nurses know which ten patients are currently admitted, so those charts stay close at hand.
- **The write-ahead log** is the requirement that every action taken (medication given, procedure performed) is first written in the daily log book at the nurse's station *before* the patient's actual chart is updated. If the hospital's records room burns down overnight, the daily log book (kept in a fireproof safe) lets you reconstruct exactly what happened to each patient.
- **A transaction** is a complete medical procedure: prep the patient, administer the drug, record the vitals, discharge instructions. If the power goes out halfway through writing up the chart, you don't want the chart to show the drug was given but not the discharge instructions — either the whole procedure's paperwork is recorded, or none of it is (atomicity).
- **Isolation** is the rule that two doctors updating the same patient's chart at the same time each see a consistent version of "the chart as it was when I started," rather than a half-edited mashup of both doctors' scribbles.

---

## How It Works Internally

### Step-by-Step: What Happens When You Run `UPDATE accounts SET balance = balance - 100 WHERE id = 7;`

```
1. Client sends SQL text over the wire (TCP connection to the DB server)
        |
        v
2. Parser tokenizes and parses the SQL into an AST
        |
        v
3. Analyzer resolves "accounts" and "id" against the system catalog,
   checks the user has UPDATE privilege on this table
        |
        v
4. Planner/Optimizer decides HOW to find id=7:
   - Is there an index on id? (usually yes, it's the primary key)
   - Cost estimate: index scan, expected 1 row -> chosen plan
        |
        v
5. Executor:
     a. Uses the primary key index (B-tree) to locate the page containing id=7
     b. Reads the page into the buffer pool (from cache if already resident)
     c. Under MVCC: creates a NEW row version with balance-100,
        marks the old version as superseded (but not yet deleted)
     d. Appends a WAL record describing this change
        |
        v
6. On COMMIT:
     a. WAL record is fsynced to disk (durable point)
     b. Locks (if any) are released
     c. Client receives "UPDATE 1"
        |
        v
7. Asynchronously, a background process (checkpointer / page cleaner)
   flushes the modified page from the buffer pool to the actual data file on disk
        |
        v
8. Later, a background VACUUM (Postgres) or compaction (LSM systems)
   reclaims space from the old, superseded row version
```

### Crash Recovery

If the server crashes between step 6 and step 7, the data file on disk still has the *old* balance — but the WAL has the durable record of the change. On restart:

```
1. Database starts up, detects an unclean shutdown
2. Reads the WAL from the last checkpoint forward
3. REDO: reapplies all committed transactions found in the WAL
   that hadn't yet made it to the data files
4. UNDO: rolls back any changes from transactions that were
   in progress but never committed
5. Database is now in a consistent state — crash recovery complete
```

This REDO/UNDO recovery algorithm (formalized as **ARIES** — Algorithm for Recovery and Isolation Exploiting Semantics — by C. Mohan et al. at IBM, 1992) is, in some form, the recovery algorithm used by essentially every mainstream relational database today.

---

## Components and Architecture

```
                       +--------------------+
   Client (app) -----> |  Connection Handler |
                       +----------+---------+
                                  |
                                  v
                       +--------------------+
                       |   Query Parser     |
                       +----------+---------+
                                  v
                       +--------------------+
                       | Query Planner /    |
                       | Optimizer          |
                       +----------+---------+
                                  v
                       +--------------------+
                       |     Executor       |
                       +----------+---------+
                                  v
        +--------------+  reads/writes  +------------------+
        | Buffer Pool  |<-------------->| Storage Engine    |
        | (page cache) |                | (B-tree/LSM,      |
        +--------------+                |  data files)      |
                |                       +------------------+
                v
        +--------------+
        | Write-Ahead  |
        | Log (WAL)    |
        +--------------+
                |
                v
        +--------------+
        | Recovery /   |
        | Checkpointer |
        +--------------+
```

Additional components in most production databases: a **lock manager** (tracks row/table locks for isolation), a **transaction manager** (assigns transaction IDs, tracks commit/abort state), a **statistics collector** (feeds the optimizer), and a **replication subsystem** (streams the WAL to replicas — see the Data Replication Strategies chapter).

---

## End-to-End Flow

**Scenario:** Priya, a backend engineer at a fintech startup, deploys a new endpoint that transfers money between two accounts.

**10:14:02.100** — A mobile client calls `POST /transfer`, triggering:
```sql
BEGIN;
UPDATE accounts SET balance = balance - 500 WHERE id = 'acct_A';
UPDATE accounts SET balance = balance + 500 WHERE id = 'acct_B';
COMMIT;
```

**10:14:02.101** — The connection pooler hands the session to a worker process. The parser validates syntax in under 0.1ms.

**10:14:02.102** — The optimizer looks up `acct_A` and `acct_B` via the primary key index (both are O(log n), each resolving in roughly 3 B-tree page reads, all served from the buffer pool since these accounts were active recently — no disk I/O needed, ~0.05ms each).

**10:14:02.103** — The executor creates new MVCC row versions for both rows with updated balances, still inside the open transaction — not yet visible to other connections.

**10:14:02.104** — Both UPDATE statements append records to the in-memory WAL buffer.

**10:14:02.105** — `COMMIT` triggers an `fsync()` of the WAL to disk. This is the single slowest step in the whole transaction — typically 1–5ms on SSD-backed storage, because it's the one point where the database must wait for a physical disk guarantee rather than working from cache.

**10:14:02.108** — The commit is durable. The client receives `200 OK`. Total latency: ~8ms.

**10:14:02.150** — Meanwhile, a different client runs `SELECT balance FROM accounts WHERE id = 'acct_A'` for a dashboard. Because it started its own transaction snapshot before Priya's COMMIT finished, under MVCC it might see the *old* balance (Read Committed isolation guarantees it will see the new one if its transaction starts after the commit; Repeatable Read might not, until it starts a new transaction).

**10:14:03.000** — In the background, the checkpointer process flushes the dirty pages for `acct_A` and `acct_B` to the actual data files on disk, decoupled from the client's request path entirely.

**10:14:10.000** — A background autovacuum process (PostgreSQL) notices the old row versions for `acct_A`/`acct_B` are no longer visible to any active transaction and reclaims that space.

---

## Production Engineering Perspective

### Scalability
Vertical scaling (bigger machine, more RAM for the buffer pool) is the first lever. Beyond that: **read replicas** for read-heavy workloads, **partitioning/sharding** for write-heavy workloads that outgrow a single node, and **connection pooling** (PgBouncer, ProxySQL) because each database connection consumes real memory and every additional connection increases context-switching overhead.

### Reliability
Reliability depends on the WAL, replication, and regular backups (see the Backup, Recovery, and Durability chapter). A single-node database with no replica and no WAL archiving is one disk failure away from total data loss.

### Performance
The buffer pool hit ratio is the single most important performance metric — if your working set doesn't fit in RAM, every query pays disk latency. Index selection, query plan quality (checked via `EXPLAIN ANALYZE`), and avoiding N+1 query patterns from application code dominate real-world performance issues far more than raw hardware.

### Availability
High availability requires more than one node: a standby replica that can be promoted (failover), or a multi-node consensus-based cluster (CockroachDB, Spanner) that tolerates node loss transparently. Single-node databases have a hard availability ceiling — restarting for a routine OS patch is downtime.

### Maintainability
Schema migrations, index bloat, table statistics staleness (`ANALYZE`), and vacuum/compaction backlogs are the quiet maintenance burdens that, ignored for months, produce sudden and mysterious performance cliffs. Treat database maintenance operations as first-class, monitored, scheduled work — not an afterthought.

---

## Tradeoffs

### Benefits

| Benefit | Explanation |
|---|---|
| Durability guarantees | WAL + fsync means committed data survives crashes |
| Strong consistency (ACID) | Application code doesn't have to reimplement correctness |
| Declarative querying (SQL) | Optimizer figures out the "how," you specify the "what" |
| Mature tooling | Decades of operational knowledge, monitoring, backup tooling |
| Rich indexing | B-trees, GIN, GiST, full-text, geospatial indexes all built-in |

### Drawbacks

| Drawback | Explanation |
|---|---|
| Vertical scaling ceiling | A single-node relational DB eventually hits CPU/RAM/disk limits |
| Write amplification | Both indexes and WAL/compaction multiply the physical I/O per logical write |
| Operational complexity | Backups, replication, failover, vacuum/compaction all require expertise |
| Schema rigidity | Changing a large table's schema can require careful, sometimes locking, migrations |

### Limitations

No single storage engine is optimal for every workload. B-trees favor balanced read/write workloads; LSM-trees favor write-heavy workloads but cost more on reads and background compaction CPU. Query optimizers are heuristic — they can and do pick bad plans, especially with stale statistics or unusual data distributions (skew).

### Alternatives

| Alternative | When to use instead |
|---|---|
| Key-value store (Redis, DynamoDB) | Simple access patterns, extreme latency requirements, no need for joins |
| Columnar analytical store (ClickHouse, BigQuery) | Aggregation over billions of rows, not point lookups |
| Search engine (Elasticsearch) | Full-text/fuzzy search is the primary access pattern |
| Object storage (S3) | Large blobs, infrequent access, no need for transactions |
| Event log (Kafka) | Append-only stream processing rather than query-and-update |

### When NOT to Use a Traditional Relational Database

- Storing large binary blobs (videos, images) directly as row data — use object storage and store a reference.
- Extremely high write throughput of simple, immutable events (e.g., clickstream logging) — an append-only log or LSM-based store is usually cheaper and faster.
- Search-heavy workloads with fuzzy matching, ranking, and relevance scoring — a purpose-built search engine will outperform SQL `LIKE` queries by orders of magnitude.

---

## Common Mistakes

### Beginner
1. **Not using transactions for multi-step operations**, leaving the database in an inconsistent state if the second statement fails.
2. **Adding indexes on every column "just in case,"** not realizing each index slows down every write to that table.
3. **Using `SELECT *`** in production code, fetching unnecessary columns and defeating covering-index optimizations.

### Intermediate
4. **Ignoring `EXPLAIN ANALYZE`** and guessing why a query is slow instead of reading the actual execution plan.
5. **N+1 queries** — issuing one query per row in a loop from application code instead of a single JOIN or batched query.
6. **Not understanding isolation levels**, leading to surprising bugs like lost updates under Read Committed when Serializable was needed (e.g., double-booking a seat).

### Senior-Level
7. **Sharding too early or with the wrong key**, creating hot shards and cross-shard transactions that are far more expensive than the single-node problem being avoided.
8. **Letting long-running transactions hold back vacuum/compaction**, causing table and index bloat that silently degrades performance over weeks until a crisis.
9. **Treating replication lag as zero** in application logic (e.g., reading your own write from a replica immediately after writing to the primary and getting stale data).

---

## Failure Scenarios

### Scenario 1: Disk Fills Up Mid-Write
**What happens:** The WAL cannot be appended to; new transactions fail; existing connections may hang.
**Why it fails:** Databases assume unbounded disk space for WAL and data files; when that assumption breaks, the failure mode is often ungraceful.
**How to diagnose:** Disk usage alerts, `ERROR: could not write to file` in logs, WAL directory growth (often caused by a stuck replication slot or a long-running transaction preventing WAL cleanup).
**Solutions:** Monitor disk usage with alerting well before capacity; set `max_wal_size` and monitor replication slot lag; keep a headroom buffer (never run below ~20% free disk).

### Scenario 2: Missing Index Causes Sequential Scan Under Load
**What happens:** A query that used to be fast starts taking seconds as a table grows past the point where a sequential scan is "cheap enough," saturating CPU and I/O, and cascading into connection pool exhaustion.
**Why it fails:** The optimizer correctly chose a sequential scan when the table was small (it was genuinely cheaper), but nobody revisited the plan as the table grew 100x.
**How to diagnose:** `EXPLAIN ANALYZE` shows `Seq Scan` on a large table; `pg_stat_statements` shows the query's total time dominating the workload.
**Solutions:** Add the appropriate index; consider partial or covering indexes; set up automated slow-query monitoring with plan regression alerts.

### Scenario 3: Lock Contention / Deadlocks Under Concurrency
**What happens:** Two transactions update the same two rows in opposite order, each waiting on a lock the other holds — the database detects and aborts one (deadlock), or, worse, without detection, both hang indefinitely.
**Why it fails:** Application code doesn't consistently order its updates (e.g., always update the lower account ID first), so lock acquisition order varies by request.
**How to diagnose:** `deadlock detected` errors in logs; spikes in `pg_locks` wait events; transaction duration percentiles spiking.
**Solutions:** Enforce a consistent lock acquisition order across the codebase; keep transactions short; use `SELECT ... FOR UPDATE` deliberately and minimally; consider optimistic concurrency (version columns) for high-contention rows.

### Scenario 4: Crash Recovery Takes Too Long
**What happens:** After an unclean shutdown, the database takes 40 minutes to replay the WAL before it can accept connections, causing extended downtime.
**Why it fails:** Checkpoints were too infrequent, so a huge amount of WAL had accumulated since the last checkpoint, and all of it must be replayed.
**How to diagnose:** Recovery logs showing "redo starts at LSN X," a large gap between last checkpoint LSN and crash LSN.
**Solutions:** Tune checkpoint frequency/size (`checkpoint_timeout`, `max_wal_size` in Postgres) to bound worst-case recovery time; test recovery time periodically as part of DR drills.

---

## Security Considerations

- **SQL injection** remains one of the most common and severe vulnerabilities in web applications. Always use parameterized queries/prepared statements — never string-concatenate user input into SQL.
- **Least-privilege database roles**: application connections should use accounts with only the permissions they need (no `SUPERUSER` for a web app connection); separate read-only roles for reporting.
- **Encryption at rest and in transit**: TLS for client connections; disk/volume encryption for data files and WAL archives, especially important for backups stored off-site.
- **Audit logging**: track schema changes and privileged operations (`pgaudit`, MySQL's audit plugin) for compliance and forensic investigation.
- **Row-level security**: modern databases (PostgreSQL RLS) can enforce that a query only sees rows the current user is authorized to see, at the database layer rather than trusting application code to filter correctly every time.

---

## Performance Considerations

### Bottlenecks

| Bottleneck | Cause | Fix |
|---|---|---|
| Buffer pool too small | Working set exceeds RAM | Increase memory, or reduce working set (archiving, partitioning) |
| Missing/unused indexes | Query planner forced into scans | Add targeted indexes; drop unused ones (they cost writes for nothing) |
| Lock contention | Hot rows updated by many transactions | Shorter transactions, optimistic concurrency, queueing |
| WAL fsync latency | Slow disks, synchronous replication | Use SSD/NVMe; tune synchronous_commit carefully |
| Connection overhead | Too many short-lived connections | Connection pooling (PgBouncer, ProxySQL) |

### Optimization Strategies
1. Index the columns actually used in `WHERE`, `JOIN`, and `ORDER BY` clauses — and nothing more.
2. Use `EXPLAIN ANALYZE` before and after any significant query change.
3. Batch writes where possible instead of issuing thousands of tiny transactions.
4. Keep transactions as short as possible to reduce lock hold time and vacuum/compaction pressure.
5. Periodically run `ANALYZE` (or your engine's statistics refresh) so the optimizer has accurate cardinality estimates.

### Scaling Challenges
Vertical scaling has a ceiling; horizontal scaling (sharding, read replicas) introduces cross-node consistency and operational complexity. Connection limits, replication lag, and hot partitions are the most common scaling pain points encountered in practice.

---

## Real-World Industry Examples

**PostgreSQL at Instagram** — Instagram famously scaled a sharded PostgreSQL architecture to serve hundreds of millions of users, using custom sharding logic at the application layer and PL/Python for ID generation, long before dedicated NewSQL systems were mature. Their engineering blog documented aggressive use of partial indexes and careful schema design to keep write amplification manageable.

**MySQL at Facebook (Meta)** — Meta operates one of the largest MySQL deployments in the world, and built **MyRocks**, an LSM-tree-based storage engine (based on RocksDB) as a drop-in replacement for InnoDB, specifically to reduce storage space and write amplification at their scale — a direct real-world example of the B-tree vs. LSM-tree tradeoff playing out in production.

**Google Spanner** — Combines a B-tree-like storage layer (based on Bigtable's SSTable lineage) with globally synchronized clocks (TrueTime) to offer externally consistent distributed transactions, demonstrating that ACID guarantees can be extended (at real engineering cost) across a planet-scale distributed system.

**Uber's migration from Postgres to MySQL (2016)** — Uber published a widely discussed engineering blog post explaining their move from PostgreSQL to MySQL, citing (at the time) issues with how Postgres's MVCC implementation interacted with their replication and upgrade patterns. It's a frequently cited case study (and later, frequently critiqued/re-examined) in understanding storage engine tradeoffs under real operational pressure.

**SQLite everywhere** — SQLite, written by D. Richard Hipp, is embedded in essentially every smartphone, browser, and desktop OS in existence, demonstrating that a single-file, B-tree-based, ACID-compliant database can serve as reliable local storage without a server process at all — it's plausibly the most widely deployed database engine on Earth by installation count.

---

## Case Studies

### Case Study 1: GitLab's Database Incident (2017)
**What happened:** During an attempt to fix replication lag on a production PostgreSQL replica, an engineer accidentally ran `rm -rf` on the wrong directory — the primary's data directory — deleting roughly 300GB of production data.
**Root cause:** A combination of unclear terminal context (which host the engineer believed they were on), and — critically — backups had been silently failing for weeks, and the standard replication/snapshot mechanisms in place were not actually producing restorable backups.
**Solution:** GitLab restored from a 6-hour-old snapshot that happened to exist from an unrelated manual process, losing roughly 6 hours of data (issues, comments, merge requests).
**Lesson:** Durability guarantees inside the database (WAL, replication) do not protect you from operational mistakes outside it. Backups must be tested by actually restoring them, not assumed to work.

### Case Study 2: Knight Capital's $440 Million Loss (2012)
**What happened:** A deployment error left old test code active in production trading systems. Combined with database/state management issues around order tracking, the system executed unintended trades at a catastrophic rate, losing $440 million in 45 minutes.
**Root cause:** Not a database bug per se, but a textbook illustration of what happens when systems lack strong transactional guarantees and consistency checks around critical, high-stakes state — state that should have been atomically and consistently tracked was allowed to drift.
**Solution:** Knight Capital was acquired shortly after; the industry response included stricter regulatory requirements (SEC Rule 15c3-5) around pre-trade risk controls and system testing.
**Lesson:** When state changes have real financial consequences, atomicity and consistency aren't academic ACID trivia — they are the difference between a company surviving the day.

### Case Study 3: MySQL's Default Isolation Level Surprise (Common Industry Pattern)
**What happened:** Numerous companies (documented across multiple engineering blogs, including Percona's) have hit subtle bugs from MySQL/InnoDB's default `REPEATABLE READ` isolation level combined with gap locking, causing unexpected deadlocks in high-concurrency insert-heavy workloads (e.g., unique constraint checks on rapidly inserted rows).
**Root cause:** Engineers assumed isolation level defaults behaved like PostgreSQL's (`READ COMMITTED` default), and were surprised by MySQL's different default and its next-key/gap-locking behavior under `REPEATABLE READ`.
**Solution:** Explicitly choosing and documenting the isolation level per workload, and in some cases switching hot-path tables to `READ COMMITTED` to reduce gap-lock contention.
**Lesson:** ACID guarantees are configurable, and defaults differ meaningfully between database systems — never assume behavior transfers directly from one engine to another.

---

## Practical Code Examples

### A Transaction with Explicit Isolation (PostgreSQL)

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

UPDATE accounts SET balance = balance - 500 WHERE id = 'acct_A';
UPDATE accounts SET balance = balance + 500 WHERE id = 'acct_B';

-- Application-level invariant check
SELECT balance FROM accounts WHERE id = 'acct_A';
-- if balance < 0, ROLLBACK instead of COMMIT

COMMIT;
```

### Inspecting a Query Plan

```sql
EXPLAIN ANALYZE
SELECT o.id, o.total, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at > now() - interval '7 days'
ORDER BY o.created_at DESC
LIMIT 50;

-- Look for: Seq Scan (bad on large tables), actual rows vs estimated rows
-- (large discrepancy = stale statistics), and total execution time.
```

### Creating a Targeted Index

```sql
-- Composite index matching the WHERE + ORDER BY pattern above
CREATE INDEX CONCURRENTLY idx_orders_created_at
ON orders (created_at DESC);

-- Partial index: only index the subset of rows actually queried often
CREATE INDEX CONCURRENTLY idx_orders_pending
ON orders (customer_id)
WHERE status = 'pending';
```

### A Minimal WAL-Like Append-Only Log (Python, illustrative)

```python
import json
import os
import time

class SimpleWAL:
    def __init__(self, path="wal.log"):
        self.path = path

    def append(self, operation: dict):
        record = json.dumps({"ts": time.time(), **operation})
        with open(self.path, "a") as f:
            f.write(record + "\n")
            f.flush()
            os.fsync(f.fileno())  # force to physical disk before returning

    def replay(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path) as f:
            return [json.loads(line) for line in f if line.strip()]

wal = SimpleWAL()
wal.append({"op": "UPDATE", "table": "accounts", "id": "acct_A", "delta": -500})
wal.append({"op": "UPDATE", "table": "accounts", "id": "acct_B", "delta": 500})
# On crash + restart: wal.replay() gives you everything needed to rebuild state
```

### Avoiding N+1 Queries

```sql
-- BAD: one query per order in application code (N+1)
-- SELECT * FROM orders WHERE customer_id = ?  (run once per customer, in a loop)

-- GOOD: a single batched query
SELECT * FROM orders WHERE customer_id = ANY(%(customer_ids)s);
```

---

## Frequently Asked Questions

**Q: Why is a WAL faster than just writing directly to the data files?**
Because the WAL is append-only and sequential — the disk head (or SSD controller) never has to seek around; it just keeps writing to the end of a file. Updating data pages in place requires random I/O across the file, which is much slower, especially on spinning disks and even measurably slower on SSDs due to write amplification.

**Q: Do I need an index on every foreign key?**
Usually yes for columns you frequently filter or join on, but not automatically for every foreign key — it depends on your query patterns. Unindexed foreign keys are a common cause of slow cascading deletes and slow joins, but indexes aren't free, so add them deliberately based on actual query patterns, not by default.

**Q: What's the real difference between B-trees and LSM-trees in practice?**
B-trees give you predictably fast reads and moderate write throughput with in-place updates. LSM-trees give you very fast, sequential write throughput at the cost of read amplification (checking multiple files) and background compaction CPU/I/O cost. Choose based on your read:write ratio.

**Q: Why does `EXPLAIN ANALYZE` sometimes show a different plan than `EXPLAIN` alone?**
`EXPLAIN` alone shows the planner's estimated plan without running the query. `EXPLAIN ANALYZE` actually executes the query and shows real timing and row counts alongside the plan, which is essential for spotting cases where the optimizer's estimates were wrong (usually due to stale statistics).

**Q: Is NoSQL "not a database" in the sense described here?**
NoSQL systems are absolutely databases — they just make different tradeoffs, often relaxing ACID guarantees or the relational model in exchange for horizontal scalability or schema flexibility. Many NoSQL systems (Cassandra, RocksDB-based stores) still use the same LSM-tree storage engine concepts described here internally. See the SQL vs NoSQL chapter for the deeper comparison.

**Q: How does a database guarantee durability if the operating system itself buffers disk writes?**
By calling `fsync()` (or equivalent), which instructs the OS to flush its write buffers all the way to physical storage before returning. Some storage hardware also has its own write cache that must be configured correctly (or backed by a battery/capacitor) for `fsync()` to be a true durability guarantee — this is a frequent, subtle source of "we thought we had durability but didn't" incidents.

---

## Interview Questions

### Beginner

**Q1: What does ACID stand for, and give a one-sentence definition of each.**
Atomicity (all-or-nothing execution of a transaction), Consistency (the database moves between valid states, respecting constraints), Isolation (concurrent transactions don't observe each other's incomplete work), Durability (committed data survives crashes).

**Q2: What is an index, and what is the tradeoff of adding one?**
An index is a secondary sorted structure (usually a B-tree) that lets the database find rows matching a condition without scanning the whole table, dramatically speeding up reads. The tradeoff is that every write to an indexed column must also update the index, slowing down inserts/updates/deletes and consuming additional storage.

**Q3: Why does a database use a write-ahead log instead of writing directly to the data files?**
Because sequential log writes are fast and let the database durably record a commit without waiting for the (slower, random-I/O) data page updates to complete. It also enables crash recovery: replaying the log rebuilds any state that didn't make it to the data files before a crash.

### Intermediate

**Q4: Explain the difference between a B-tree and an LSM-tree storage engine, and when you'd choose each.**
A B-tree keeps data sorted in a balanced tree of fixed-size pages, updated in place — good for balanced or read-heavy workloads with consistently low read latency. An LSM-tree buffers writes in memory, flushes them as immutable sorted files, and merges them later via compaction — excellent write throughput (all sequential I/O) at the cost of read amplification and background compaction overhead. Choose B-trees for typical OLTP apps with mixed reads/writes; choose LSM-trees for write-heavy workloads like logging, time-series, or high-ingest event pipelines.

**Q5: What is MVCC and why do most modern relational databases use it instead of pure locking?**
MVCC (Multi-Version Concurrency Control) lets readers see a consistent snapshot of data without blocking writers, and vice versa, by keeping multiple versions of a row and giving each transaction a consistent view as of its start time. This dramatically improves concurrency compared to pure lock-based isolation, where readers and writers would otherwise block each other constantly.

**Q6: What happens, step by step, if a database server crashes mid-transaction?**
On restart, the recovery process reads the WAL from the last checkpoint. It REDOes any committed transactions whose data-page changes hadn't yet been flushed to disk, and UNDOes any transactions that were in progress but never committed, bringing the database back to a consistent state reflecting exactly the set of transactions that were durably committed before the crash.

### Senior

**Q7: A query that was fast last month is now taking 10 seconds. Walk through your diagnostic process.**
Start with `EXPLAIN ANALYZE` to see the actual execution plan and compare estimated vs. actual row counts (large gaps suggest stale statistics — run `ANALYZE`). Check whether the table has grown significantly, whether an index that used to be used is no longer chosen (or was dropped), whether there's lock contention (check `pg_locks`/equivalent), and whether the buffer pool hit ratio has dropped (working set no longer fits in memory). Also check for a recent schema or query change, and confirm the query isn't now scanning a much larger date range or joining against a table that's grown non-linearly.

**Q8: How would you design the schema and indexing strategy for a table that receives 50,000 writes/second and needs point lookups by ID with p99 < 5ms?**
At that write rate, I'd lean toward an LSM-tree-based engine (or a B-tree engine tuned heavily for write throughput, e.g., wide buffer pool, aggressive checkpoint tuning) and minimize the number of secondary indexes since each one adds write amplification. I'd consider partitioning/sharding by a high-cardinality key to spread write load across multiple nodes, use a small number of covering indexes only for the actual hot query patterns, and validate the design against a realistic load test rather than assumptions, since write-heavy workloads often reveal compaction/checkpoint bottlenecks that don't show up at lower throughput.

### Architecture

**Q9: Design the storage layer for a multi-tenant SaaS application with wildly uneven tenant sizes (some tenants have 10 rows, others have 100 million).**
I'd avoid a single giant shared table with a `tenant_id` column and no further isolation, since it creates noisy-neighbor problems and uneven index sizes. Options: (1) schema-per-tenant for large tenants combined with shared tables for small tenants (hybrid), (2) partition large tables by `tenant_id` range or hash, (3) monitor per-tenant table/index size and proactively "graduate" a growing tenant to its own partition or shard. I'd also ensure indexes always lead with `tenant_id` so queries stay scoped, and set up per-tenant resource governance (connection limits, query timeouts) to prevent one large tenant's load from starving others.

**Q10: Your team wants to migrate from a single PostgreSQL instance to a horizontally sharded architecture. What are the key risks and how do you mitigate them?**
Key risks: cross-shard transactions become expensive or impossible with strict ACID guarantees (mitigate with careful shard-key selection so most transactions stay single-shard, and use sagas/two-phase commit sparingly for the rest); rebalancing shards as data grows unevenly (mitigate with consistent hashing or range-based resharding tooling built in from day one); increased operational complexity (mitigate with strong automation for schema migrations across all shards, and centralized observability). I'd also strongly consider whether a NewSQL system (CockroachDB, Spanner, YugabyteDB) that handles sharding and distributed transactions natively is a better investment than building custom sharding logic in-house, given the significant engineering cost of doing it correctly.

---

## In the AI Era

Two AI-era developments touch database internals directly.

**1. Vector search is now a database feature.** Embeddings turn text, images, or code into high-dimensional vectors where "similar meaning" becomes "nearby points." Finding the nearest neighbors exactly is too slow at scale, so databases use **approximate nearest neighbor (ANN)** indexes such as HNSW (a layered graph) and IVF (clustering into buckets). These trade a little *recall* (occasionally missing a true neighbor) for large speedups — the same kind of tradeoff as choosing a B-tree versus a hash index. Many general-purpose databases now support vector indexes directly (for example, PostgreSQL through the pgvector extension).

**2. LLMs write queries.** "Text-to-SQL" features and coding assistants generate SQL constantly. Everything in this chapter about query planning still decides whether that SQL is fast or catastrophic. Guardrails for model-generated queries:

- Use a **read-only database role** with access to only the needed tables or views.
- Set **statement timeouts** and row limits.
- Run **`EXPLAIN`** on generated queries in development; a missing index doesn't care who wrote the query.
- Never interpolate model output into SQL strings — generated values go through parameters like any other untrusted input.

**Try it:** Ask an assistant to write a query for a reporting question on one of your schemas. Run `EXPLAIN ANALYZE` on it. Does it use the indexes you expect? Could you have predicted the plan from this chapter?

---

## Key Takeaways

1. A database is four systems in one: a storage engine, a query engine, a transaction/concurrency manager, and a recovery system.
2. B-trees and LSM-trees represent the two dominant storage engine philosophies — in-place balanced updates vs. append-only sequential writes with background compaction.
3. Indexes trade write cost for read speed; adding indexes indiscriminately is one of the most common real-world performance mistakes.
4. Every query passes through parsing, analysis, planning/optimization, and execution — `EXPLAIN ANALYZE` is your window into that pipeline.
5. ACID transactions exist to let application code stop worrying about partial failures and concurrent interference.
6. MVCC lets readers and writers avoid blocking each other by maintaining multiple row versions, which is why modern relational databases can serve high concurrency without collapsing into lock contention.
7. The write-ahead log is what makes durability affordable: sequential log writes are fast, and crash recovery replays the log rather than requiring every write to be synchronously flushed to its final location.
8. No storage engine is universally best — the right choice depends on your read:write ratio, consistency requirements, and scale.
9. Database internals knowledge is directly actionable: it explains why a query is slow, why a crash didn't lose data, and why an index didn't help.
10. Operational practices (backups, statistics maintenance, vacuum/compaction, monitoring) matter as much as the underlying algorithms — a theoretically sound database can still lose data or degrade badly if operated carelessly.

---

## Further Reading

### Foundational Papers
- Codd, E.F. — *"A Relational Model of Data for Large Shared Data Banks"* (1970): https://dl.acm.org/doi/10.1145/362384.362685
- O'Neil, Cheng, Gawlick, O'Neil — *"The Log-Structured Merge-Tree (LSM-Tree)"* (1996): https://www.cs.umb.edu/~poneil/lsmtree.pdf
- Mohan et al. — *"ARIES: A Transaction Recovery Method"* (1992): https://dl.acm.org/doi/10.1145/128765.128770
- Gray, Jim — *"The Transaction Concept: Virtues and Limitations"* (1981): https://www.eecs.harvard.edu/~htk/publication/1981-icvldb-gray.pdf
- Chang et al. — *"Bigtable: A Distributed Storage System for Structured Data"* (2006): https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/

### Academic Resources
- CMU 15-445/645 — Database Systems (Andy Pavlo): https://15445.courses.cs.cmu.edu/
- MIT 6.830 — Database Systems: https://dsg.csail.mit.edu/6.830/
- Berkeley CS 186 — Introduction to Database Systems: https://cs186berkeley.net/

### Industry Engineering Blogs
- PostgreSQL Wiki, "Why is Postgres Slow": https://wiki.postgresql.org/wiki/Slow_Query_Questions
- Meta Engineering — MyRocks: https://engineering.fb.com/category/data-infrastructure/
- Uber Engineering — "Why Uber Engineering Switched from Postgres to MySQL": https://www.uber.com/blog/postgres-to-mysql-migration/
- Percona Database Performance Blog: https://www.percona.com/blog/

### Official Documentation
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- MySQL/InnoDB Documentation: https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html
- SQLite Documentation: https://sqlite.org/docs.html
- RocksDB Wiki: https://github.com/facebook/rocksdb/wiki

### Books
- *"Database Internals"* by Alex Petrov (O'Reilly)
- *"Designing Data-Intensive Applications"* by Martin Kleppmann (O'Reilly)
- *"Readings in Database Systems"* (the "Red Book"), edited by Peter Bailis, Joseph M. Hellerstein, Michael Stonebraker: http://www.redbook.io/

### Videos
- CMU Database Group — full lecture series on YouTube (Andy Pavlo)
- "How does a relational database work" talks from various PostgreSQL/MySQL conferences (PGCon, Percona Live)

---

*This chapter is part of the Software Engineering Handbook — a comprehensive guide to the concepts, principles, and practices that every professional software engineer should know.*
