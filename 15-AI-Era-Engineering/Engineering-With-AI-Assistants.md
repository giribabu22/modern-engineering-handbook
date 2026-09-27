# Engineering With AI Assistants: A Workflow That Holds Up

*AI makes writing code cheap. It does not make understanding, verifying, or owning code cheap.*

---

## Introduction

Two teams adopt the same AI coding assistant on the same day.

Team A measures success by output. Pull requests double in the first month. By the third month, review queues are overflowing, a string of subtle bugs has reached production, and senior engineers spend their days reviewing code that the authors themselves can't fully explain. Velocity, measured in shipped *working* features, is lower than before.

Team B treats the assistant as a powerful but junior collaborator inside an engineering process. They invest in fast tests, clear project documentation the assistant can read, and small, reviewable changes. Engineers use the assistant heavily for exploration, boilerplate, tests, and first drafts — and they own every line they merge. Their throughput rises steadily and stays up.

Same tool. Different engineering. This chapter describes the practices that make the difference.

### Why Should Engineers Care?

AI assistants — from inline autocomplete to chat assistants to autonomous coding agents that edit files and run commands — are now part of everyday development. Used well, they compress hours of work into minutes. Used carelessly, they generate code faster than a team can understand it. The skill that matters is no longer typing speed or API recall; it's **specification, decomposition, verification, and judgment**.

---

## The Problem It Solves

Much of software development time goes to work that is necessary but not intellectually demanding:

- Writing boilerplate, glue code, and configuration
- Looking up APIs and translating between formats
- Writing routine tests
- Reading unfamiliar code to find where something happens
- Drafting documentation, migration scripts, and one-off tooling

AI assistants handle much of this well. They also help with harder work — exploring designs, explaining unfamiliar code, generating debugging hypotheses — when paired with a human who can judge the output.

---

## Historical Background

- **1990s–2000s — IDE code completion.** Tools like IntelliSense completed identifiers using static analysis of types and symbols.
- **2010s — Statistical completion.** Research and products began ranking completions using models trained on code.
- **2021 — LLM-powered completion.** Large models trained on public code made multi-line, context-aware suggestions mainstream in editors, starting with GitHub Copilot's preview.
- **2022–2023 — Chat assistants.** General chat models became capable programmers, and developers began pasting code, errors, and questions into chat.
- **2024–present — Coding agents.** Assistants gained the ability to read entire repositories, edit many files, run tests and commands, and iterate on failures — working on tasks for minutes or hours with varying degrees of autonomy. Benchmarks such as SWE-bench, built from real GitHub issues, began measuring end-to-end task completion rather than single-function correctness.

The trajectory is clear: from completing *tokens*, to completing *functions*, to completing *tasks*. Each step moves the human's role further from typing and closer to specifying and reviewing.

---

## Core Concepts

### The Spectrum of Autonomy

| Mode | What the AI does | Human role | Best for |
|------|-----------------|-----------|---------|
| **Autocomplete** | Suggests the next lines as you type | Accept/reject in real time | Flow-state coding, boilerplate |
| **Chat** | Answers questions, drafts snippets | Copy, adapt, verify | Explanations, exploration, small pieces |
| **Pair agent** | Edits files and runs commands with approval | Approve each step, steer | Multi-file changes you want to watch |
| **Autonomous agent** | Works a task end to end, opens a PR | Specify up front, review the result | Well-specified tasks with strong tests |

The more autonomy you grant, the more your success depends on two things: **how well the task is specified** and **how well correctness can be checked automatically**.

### The Verification Gap

The single most important concept in AI-assisted engineering:

```
Speed of generating code  ───────────────────────────►  very fast
Speed of verifying code   ────────►                     still human-paced
                                   └── the gap ──┘
```

Everything that narrows this gap — fast tests, type checkers, linters, small diffs, clear specs, good observability — becomes dramatically more valuable. Codebases with strong automated verification get far more benefit from AI than codebases without it.

### Context Is the Input

An assistant can only be as good as the context it has. High-leverage context includes:

- **Project instructions files** (many tools read a repository-level file of conventions, commands, and architecture notes).
- **Examples of the pattern you want** ("follow the approach in `payments/refund.py`").
- **The actual error output**, not a paraphrase.
- **Constraints** — performance targets, compatibility requirements, things *not* to change.
- **Access to run the code**, so the agent can observe real behavior instead of guessing.

### Ownership

**You are the author of any code you merge**, regardless of who or what typed it. "The AI wrote it" is not an explanation in a postmortem. If you can't explain a piece of code, you're not ready to ship it.

---

## Real-World Analogy

Think of an AI assistant as a remarkably fast contractor who has read every building manual ever written but has never visited your building.

They'll frame a wall in minutes. But unless you show them the blueprints, they may put it in the wrong place; unless you tell them the building code, they may follow a different one; and unless an inspector checks the work, you won't know whether the wiring behind the drywall is sound. The best site managers give crisp specifications, keep work in small inspectable stages, and never skip inspection because the crew is fast.

---

## How It Works In Practice

### A Workflow That Scales

```
1. Understand   → Clarify the problem yourself. Use AI to explore the codebase
                   and ask questions, not yet to write the fix.
2. Specify      → Write down what "done" means: behavior, constraints, tests.
3. Plan         → Ask the assistant for a plan; review the plan before any code.
4. Implement    → Small steps. Let the agent run tests after each step.
5. Verify       → Tests, types, lint, run the thing, check edge cases yourself.
6. Review       → Read the full diff as if a stranger wrote it. Because one did.
7. Own          → Commit with a message you wrote and understand.
```

**Reviewing the plan before the code** is the highest-leverage step. A wrong approach caught in a five-line plan costs seconds; caught in a 500-line diff, it costs an hour.

### Where AI Assistance Shines

| Task | Why it works well |
|------|------------------|
| Explaining unfamiliar code | Reading is cheap to verify against the source |
| Writing tests for existing behavior | Tests are checkable by running them |
| Boilerplate and scaffolding | Low risk, well-established patterns |
| Mechanical refactors and migrations | Verifiable by compiler and tests |
| One-off scripts and internal tools | Low blast radius |
| Generating debugging hypotheses | Breadth of ideas; you run the experiments |
| Drafting docs and commit messages | Easy to review and edit |

### Where to Be Careful

| Task | Risk |
|------|-----|
| Security-sensitive code (auth, crypto, permissions) | Subtle flaws that tests rarely catch |
| Concurrency and distributed-systems logic | Bugs appear only under rare interleavings |
| Performance-critical paths | Plausible code can be asymptotically slow |
| Code using fast-moving or niche libraries | Outdated or invented APIs |
| Large, sweeping changes | Diffs too big to review meaningfully |
| Anything you can't test | No way to close the verification gap |

### Prompting for Engineering Work

Effective requests share a structure:

```
Goal:          Add rate limiting to the /export endpoint.
Context:       We use the token-bucket limiter in `middleware/ratelimit.py`
               (see how /search uses it). Redis is available.
Constraints:   Don't change the public response format. Limit per API key.
Done means:    New tests in tests/test_export.py cover: under limit, over
               limit (429 with Retry-After), and separate keys.
               All existing tests pass.
Process:       Propose a plan first. Don't write code until I approve it.
```

This is simply a good task description — the same one you'd give a new teammate. Engineers who write clear tickets get better results from AI.

---

## Production Engineering Perspective

AI assistance changes team-level dynamics, not just individual speed:

- **Review is the new bottleneck.** Keep pull requests small. Require authors to self-review AI-generated diffs before requesting human review. Consider AI-assisted review as a *first pass*, never as the only reviewer.
- **Tests are infrastructure.** A slow or flaky test suite now blocks both humans and agents. Investing in test speed and reliability pays twice.
- **Documentation compounds.** Architecture notes, conventions, and runbooks written for humans also steer agents. Teams that write things down get better AI output.
- **Consistency needs enforcement.** Formatters, linters, and architectural checks keep generated code from drifting into many styles.
- **Agents need guardrails.** Sandboxed environments, no production credentials, protected branches, and required reviews are what make autonomous agents safe to use.
- **Measure outcomes, not output.** Lines of code and PR counts are misleading. Track lead time, change failure rate, time to restore service, and escaped defects.

---

## Tradeoffs

| Choice | Benefit | Cost |
|--------|--------|-----|
| Higher agent autonomy | Less human time per task | More risk; review happens late and in bulk |
| Accepting larger AI diffs | Faster apparent progress | Weaker review, hidden bugs, lower understanding |
| Relying on AI for unfamiliar domains | Fast ramp-up | You may not recognize wrong answers |
| Heavy AI use by early-career engineers | Productivity now | Risk of skipping the struggle that builds deep skill |
| Strict "no AI" policies | Predictability | Lost productivity; shadow usage without guardrails |

On learning: struggle is how expertise forms. Early-career engineers benefit from using AI as a **tutor** — asking it to explain, quiz, and critique — rather than only as a generator of answers. Write the solution yourself first, then compare.

---

## Common Mistakes

1. **Accepting code you don't understand.** If you couldn't have written it with enough time, study it before merging.
2. **Letting the AI grade its own work.** "It said the tests pass" is not the same as running the tests yourself or in CI.
3. **Letting agents weaken tests to make them pass.** Watch diffs to test files carefully — deleted assertions, broadened expectations, or skipped tests are red flags.
4. **Regenerating instead of debugging.** Rerolling until something works hides the actual problem.
5. **Vague prompts, then blaming the tool.** Underspecified tasks get plausible-but-wrong results.
6. **Pasting secrets or sensitive data** into tools not approved for it.
7. **Installing suggested dependencies without checking them.** Verify that a package exists, is the one you intended, and is maintained.
8. **Huge one-shot changes.** Break work into steps that can each be verified.

---

## Failure Scenarios

### Scenario 1: The Test That Tested Nothing

An agent is asked to fix a failing test. It "fixes" it by changing the expected value to match the buggy output. CI goes green. The bug ships.

**Prevention:** review test-file diffs with extra care; state explicitly that tests define correct behavior and must not be changed without approval; keep tests in a separate commit from fixes when possible.

### Scenario 2: The Plausible Security Hole

An assistant generates a file-download endpoint that joins a user-supplied filename onto a base directory. It works perfectly in manual testing. It also allows `../../etc/passwd`.

**Prevention:** security-sensitive code gets explicit threat review; add tests for malicious inputs; use static analysis and security scanners in CI.

### Scenario 3: The Runaway Agent

An autonomous agent working on a flaky integration test decides the database fixture is "corrupted" and runs a command to reset it — against a shared staging database that another team is using for a release rehearsal.

**Prevention:** agents operate only in isolated, disposable environments; credentials are scoped to what the task requires; destructive commands require human approval enforced by the tool, not by a request in the prompt.

---

## Practical Exercises

1. **Plan review drill.** Give an assistant a medium-sized task and ask only for a plan. Find at least one flaw or missing consideration before letting it write code.
2. **Verification budget.** For your next AI-assisted change, record how long generation took and how long verification took. Which part would faster tests shrink?
3. **Explain-back.** Pick a function an assistant wrote for you last week. Without looking at it, explain what it does and its edge cases. Then check.
4. **Project context file.** Write a one-page instructions file for your repository: how to build, test, lint, the architecture in five bullet points, and conventions. Compare agent output before and after.
5. **Tutor mode.** Solve a problem yourself, then ask the assistant to critique your solution and propose alternatives. Compare what you learn to asking for the answer directly.

---

## Frequently Asked Questions

**Will AI replace software engineers?**
It is replacing some *tasks*, especially routine code production. The responsibilities that remain — understanding problems, making tradeoffs, designing systems, verifying correctness, operating software, and taking accountability — are the ones this handbook focuses on. Engineers who are strong at those become more productive, not less relevant.

**Should juniors use AI assistants?**
Yes, deliberately. Use them to learn faster (explanations, reviews, quizzes), and make sure you can solve problems without them. Being able to verify output depends on knowing how to do the work yourself.

**Is AI-generated code lower quality?**
It varies with the task, the context provided, and verification. Code merged after rigorous review and testing can be as good as any other. Code merged because "it looked fine" carries the same risks as any unreviewed code — at a much higher volume.

**How do I handle licensing and IP concerns?**
Follow your organization's policy and the tool's terms. Many enterprise tools offer controls such as filtering suggestions that match public code. When in doubt, ask your legal team.

---

## Interview Questions

### Beginner

**Q1: How do you verify code produced by an AI assistant?**

*Model answer:* The same way I'd verify any code, but without assuming competence: read and understand every line, run it, run the existing tests, add tests for edge cases the assistant didn't mention, check that any APIs it uses exist in our versions, and run linters, type checkers, and security scanners. If I can't explain it, I don't merge it.

### Intermediate

**Q2: Your team's PR volume doubled after adopting AI tools, but incidents also rose. What do you do?**

*Model answer:* Treat it as a review-capacity and verification problem. I'd reduce PR size, require author self-review of AI-generated changes, strengthen automated checks in CI (tests, types, static analysis), and look at escaped defects to find which kinds of changes are slipping through. I'd shift team metrics from output (PR count) to outcomes (change failure rate, lead time, escaped defects).

### Senior

**Q3: How would you make a codebase more effective for AI coding agents?**

*Model answer:* Improve the same things that make it good for humans, with extra weight on automation: fast, reliable, deterministic tests; clear build and test commands; type checking and linting; a concise architecture and conventions document at the repo root; consistent patterns agents can imitate; and isolated, reproducible development environments with no production access. The payoff is that agents can verify their own work before a human sees it.

### Architecture / Leadership

**Q4: What policy would you set for autonomous coding agents in your organization?**

*Model answer:* Agents run in sandboxed environments with least-privilege, task-scoped credentials and no production access; all output goes through the same PR process, CI, and human review as human-written code; destructive or externally visible actions require explicit human approval enforced by tooling; usage and spend are logged; data sent to external providers follows data-classification rules; and the human who merges owns the change. Then I'd revisit the policy regularly, because capabilities change quickly.

---

## Key Takeaways

1. AI makes producing code cheap; understanding, verifying, and owning code remain the expensive — and valuable — parts.
2. The verification gap between generation speed and verification speed decides whether AI speeds a team up or slows it down.
3. Fast tests, type checks, small diffs, and clear documentation are the highest-leverage investments for AI-assisted teams.
4. Review the plan before the code; small, verifiable steps beat large one-shot changes.
5. You own every line you merge, regardless of who or what wrote it.
6. Give agents isolated environments, least-privilege credentials, and system-enforced approval for destructive actions.
7. Measure outcomes (lead time, change failure rate, escaped defects), not output (lines, PR count).
8. Use AI as a tutor, not just a generator, to keep building the skills needed to judge its output.

---

## Further Reading

- **"No Silver Bullet — Essence and Accident in Software Engineering" (1986)** — Fred Brooks. Essential for understanding which parts of software difficulty tools can and cannot remove.
- **DORA / "Accelerate"** — Forsgren, Humble, Kim. The outcome metrics (lead time, deployment frequency, change failure rate, time to restore) to measure AI's real impact: [https://dora.dev](https://dora.dev)
- **"SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" (2023)** — Jimenez et al.: [https://arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770)
- **"Evaluating Large Language Models Trained on Code" (2021)** — Chen et al., introducing HumanEval: [https://arxiv.org/abs/2107.03374](https://arxiv.org/abs/2107.03374)
- **Your AI tool's documentation** on project instruction files, permissions, and sandboxing.
- **Simon Willison's weblog** — practical, skeptical, hands-on writing about using LLMs for programming: [https://simonwillison.net](https://simonwillison.net)

---

*This chapter is part of the Modern Software Engineering Handbook — a comprehensive guide to the concepts, principles, and practices that every professional software engineer should know.*
