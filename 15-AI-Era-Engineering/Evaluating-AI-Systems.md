# Evaluating AI Systems: Testing Software That Doesn't Give the Same Answer Twice

*If you can't measure whether a change made your AI system better, every change is a guess.*

---

## Introduction

A team tweaks the prompt for their document-extraction feature to fix a customer complaint about date formats. They try the customer's document; it works. They ship.

Two days later, a different customer reports that invoice totals are coming back empty. The new prompt fixed dates and broke totals on invoices with multiple currencies. Nobody noticed because nobody tested invoices with multiple currencies — the team had been testing by *vibes*: try a few examples, eyeball the output, ship if it looks good.

Another team makes the same kind of change, but first runs it against an **evaluation suite** of 300 real, labeled documents. The report shows dates improved from 91% to 98% correct — and multi-currency totals dropped from 95% to 60%. They fix the regression before any customer sees it.

This chapter is about being the second team.

### Why Should Engineers Care?

Traditional tests assume deterministic code: same input, same output, exact assertion. AI components break that assumption. Outputs vary between runs, "correct" is often a matter of degree, and small prompt or model changes cause unpredictable effects across many inputs. **Evaluations ("evals") are the test suites of AI systems**, and teams that invest in them iterate faster and ship with far fewer surprises.

---

## The Problem It Solves

| Traditional testing assumption | Reality for AI components |
|-------------------------------|---------------------------|
| Deterministic output | Output varies between runs |
| Exact expected values | Many acceptable answers ("summarize this") |
| Change affects code you touched | Prompt or model change can affect every behavior |
| Pass/fail per test | Quality is a rate: "correct 94% of the time" |
| Tests are cheap to run | Each case costs tokens and time |

Without evals, teams fall into predictable traps: fixing one case while breaking others, being unable to judge whether a new model is better, and arguing about quality from anecdotes.

---

## Historical Background

- **Machine learning has always used held-out test sets.** Train on one dataset, measure on another. Metrics like accuracy, precision, recall, and F1 date back decades.
- **NLP benchmarks (2000s–2010s)** such as BLEU for translation and ROUGE for summarization measured text overlap with reference answers — useful but often poorly correlated with human judgment.
- **General benchmarks for LLMs (2020s)** such as MMLU (knowledge), HumanEval (code), and SWE-bench (real software issues) compared models broadly. Public benchmarks are useful for choosing candidates but tell you little about *your* task — and can be inflated when benchmark data leaks into training data.
- **LLM-as-judge (2023–)** research, such as the MT-Bench work (Zheng et al.), showed strong models can grade open-ended outputs with reasonable agreement with humans — enabling scalable evaluation of tasks without single correct answers, along with known biases to control for.
- **Evals as engineering practice (2023–present).** Teams building AI products increasingly treat evaluation suites as core infrastructure, run in CI, on par with unit and integration tests.

---

## Core Concepts

### An Eval Is a Dataset Plus a Grader

```
Eval = [ (input, expected or criteria) , ... ]  +  grader(output, expected) → score
```

Run the system on every input, grade every output, aggregate the scores. That's it. The craft lies in choosing good cases and good graders.

### Types of Graders

| Grader | How it works | Best for | Weakness |
|-------|-------------|---------|---------|
| **Exact / programmatic** | Compare fields, run code, check schema, regex | Extraction, classification, code (run tests) | Can't judge open-ended text |
| **Reference similarity** | Compare to a reference answer (overlap, embedding similarity) | Rough regression signals | Rewards surface similarity, not correctness |
| **LLM-as-judge** | A model grades the output against a rubric | Open-ended answers: helpfulness, faithfulness, tone | Bias, variance, cost; must be validated |
| **Human review** | People grade outputs | Ground truth, calibrating other graders | Slow, expensive, inconsistent without rubrics |

**Prefer programmatic graders whenever possible.** They are fast, cheap, and deterministic. Many "subjective" qualities can be decomposed into checkable facts: does the summary mention the refund amount? Is it under 100 words? Does every citation point to a retrieved document?

### Building the Dataset

Good eval cases come from:
1. **Real production inputs** (sampled, anonymized as needed) — the most representative.
2. **Failures** — every bug report becomes an eval case, just like a regression test.
3. **Edge cases** designed deliberately: empty input, huge input, other languages, adversarial or injected instructions, ambiguous requests.
4. **Coverage of segments** — different customer types, document types, and difficulty levels, so a regression in one segment isn't hidden by the average.

Start small. **Twenty well-chosen cases beat zero.** Grow the set as you learn what fails.

### Metrics That Matter

- **Task success rate** (overall and per segment)
- **Format validity rate** (parseable, schema-conformant)
- **Faithfulness / groundedness** (claims supported by provided sources)
- **Refusal behavior** — correct refusals and incorrect refusals
- **Safety** — resistance to prompt injection and policy violations
- **Latency and cost per case**

For RAG systems, evaluate retrieval separately: **recall@k** (was the needed chunk in the top k?) tells you whether answer failures are retrieval problems.

### Handling Nondeterminism

- Run each case **multiple times** when variance matters and report the pass rate, not a single pass/fail.
- Compare versions on the **same dataset**, and treat small differences with skepticism — with 100 cases, a 2-point change may be noise.
- Consider **pass@k** (succeeds at least once in k tries) versus **pass^k** (succeeds in all k tries) — the second matters for reliability-critical features.

### Offline vs. Online Evaluation

| Offline | Online |
|--------|-------|
| Before shipping, on a fixed dataset | In production, on real traffic |
| Catches regressions early | Catches what your dataset didn't anticipate |
| Controlled and repeatable | Realistic and continuous |
| Examples: CI eval runs, model comparison | Examples: user feedback, sampled grading, A/B tests, business metrics |

You need both. Offline evals gate changes; online monitoring discovers new failure modes, which become new offline cases.

---

## Real-World Analogy

Evals are to AI systems what a tasting panel is to a restaurant kitchen.

A chef who changes a recipe tastes one spoonful and thinks it's great. A serious kitchen has a panel taste every dish on the menu against a scoring sheet — because the new spice blend that improved the soup may ruin the stew that uses the same stock. The scoring sheet (rubric) keeps tasters consistent, the full menu (dataset) catches side effects, and customer feedback (online evaluation) reveals dishes the panel never thought to test.

---

## How It Works In Practice

### The Eval-Driven Development Loop

```
     ┌──────────────────────────────────────────────┐
     │                                              │
     ▼                                              │
 Collect cases ─► Run system ─► Grade ─► Analyze failures
 (prod samples,                            │
  bug reports,                             ▼
  edge cases)                     Change prompt / retrieval /
                                  tools / model
                                           │
                                           ▼
                                  Re-run full eval ─► Ship only if
                                                      no segment regressed
```

This mirrors test-driven development: define what "good" means, then iterate against it.

### Read the Failures

Aggregate scores tell you *whether* something changed; reading failed outputs tells you *why*. Teams that regularly read raw outputs — dozens at a time — find failure patterns ("it ignores the second table," "it answers in English when asked in Spanish") that no metric reveals. Categorize failures, count them, and fix the biggest category first.

### Validate Your LLM Judge

An LLM judge is itself a model that can be wrong. Before trusting it:
1. Have humans grade a sample (e.g., 50–100 outputs).
2. Run the judge on the same sample.
3. Measure agreement. Adjust the rubric until agreement is acceptable.
4. Re-check periodically, especially after changing the judge model.

Known judge biases include favoring longer answers, favoring outputs from similar models, and sensitivity to the order in which options are presented. Mitigate with specific rubrics, binary or low-granularity scores, asking for reasoning before the verdict, and swapping order in pairwise comparisons.

---

## Production Engineering Perspective

- **Run evals in CI** on every change to prompts, retrieval, tools, or model versions. Use a fast subset on every PR and the full suite before release.
- **Version everything together:** prompt, model version, retrieval configuration, and eval results. A model upgrade is a deployment; treat it like one.
- **Gate releases on per-segment thresholds**, not only on the overall average.
- **Canary and shadow deployments:** send a small share of traffic to the new version, or run it in parallel without showing results, and compare.
- **Monitor production quality** with sampled grading, user feedback, and downstream signals (edits, escalations, retries, abandonment).
- **Close the loop:** production failures become eval cases within days, not quarters.
- **Budget for evals.** Evals cost tokens. Use smaller subsets for iteration, cache outputs for unchanged configurations, and run full suites when it matters.

---

## Tradeoffs

| Choice | Tradeoff |
|-------|---------|
| Small dataset vs. large | Fast and cheap vs. statistically meaningful and broad |
| Programmatic vs. LLM judge | Reliable and cheap vs. flexible for open-ended quality |
| Synthetic vs. real cases | Easy to generate at scale vs. representative of real users |
| Strict gates vs. judgment | Prevents regressions vs. may block net-positive changes |
| Frequent full runs vs. sampled runs | Confidence vs. cost and time |

Synthetic cases generated by a model are useful for coverage, but review them: they tend to be cleaner and more uniform than real inputs.

---

## Common Mistakes

1. **Testing by vibes** — a few manual examples before shipping.
2. **Relying on public benchmarks** to choose a model for a specific task.
3. **Only tracking the average,** hiding regressions in important segments.
4. **Never reading raw outputs.**
5. **Trusting an unvalidated LLM judge.**
6. **Overfitting to the eval set,** tweaking prompts until the specific cases pass while real quality stays flat. Keep a held-out set.
7. **Letting the eval set go stale** as the product and users change.
8. **No safety or adversarial cases,** so prompt-injection regressions slip through.

---

## Failure Scenarios

### Scenario 1: The Averaged-Away Regression

A new model improves the overall score from 88% to 91%. The release ships. Enterprise customers — 8% of cases but 60% of revenue — drop from 93% to 79% because the new model handles long, table-heavy documents worse.

**Prevention:** segment metrics by customer type, document type, and length; gate on each important segment.

### Scenario 2: The Lenient Judge

An LLM judge rates 97% of support answers as "helpful." Human review of a sample finds 20% contain a factual error about policy. The rubric asked about tone and completeness but never checked factual accuracy against sources.

**Prevention:** validate judges against human labels; decompose rubrics into specific checks (e.g., "Is every policy claim supported by the provided policy text?").

### Scenario 3: The Contaminated Benchmark

A team picks a model because it tops a public benchmark closely resembling their task. It underperforms in production. The benchmark's test data had been widely published and likely influenced training.

**Prevention:** make the final choice based on your own private eval set, built from your own data.

---

## Practical Code Examples

### A Minimal Eval Harness

```python
import json
import statistics
from collections import defaultdict

def load_cases(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]      # JSONL: one case per line

def grade_extraction(output: dict, expected: dict) -> dict:
    """Programmatic grader: per-field correctness."""
    return {field: output.get(field) == value for field, value in expected.items()}

def run_eval(system, cases, runs_per_case=3):
    by_segment = defaultdict(list)
    failures = []
    for case in cases:
        for _ in range(runs_per_case):
            try:
                output = system(case["input"])
                fields = grade_extraction(output, case["expected"])
                passed = all(fields.values())
            except Exception as exc:                  # invalid JSON, timeouts, etc.
                passed, fields = False, {"error": repr(exc)}
            by_segment[case.get("segment", "all")].append(passed)
            if not passed:
                failures.append({"id": case["id"], "fields": fields})

    report = {seg: round(statistics.mean(r), 3) for seg, r in by_segment.items()}
    return report, failures

def gate(new_report, baseline_report, max_drop=0.02):
    """Fail the build if any segment regresses by more than max_drop."""
    regressions = {
        seg: (baseline_report[seg], score)
        for seg, score in new_report.items()
        if seg in baseline_report and baseline_report[seg] - score > max_drop
    }
    if regressions:
        raise SystemExit(f"Eval regression: {regressions}")
```

### An LLM-as-Judge Grader With a Specific Rubric

```python
JUDGE_PROMPT = """You are grading a customer-support answer.

Source policy text:
<policy>{policy}</policy>

Customer question:
<question>{question}</question>

Answer to grade:
<answer>{answer}</answer>

Check each criterion. Explain your reasoning briefly, then output JSON:
{{"supported_by_policy": true|false,   // every factual claim appears in the policy
  "answers_the_question": true|false,
  "invents_no_policy": true|false}}"""

def judge(llm, policy, question, answer) -> dict:
    response = llm.complete(
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(
            policy=policy, question=question, answer=answer)}],
        temperature=0,
    )
    verdict = json.loads(response.text[response.text.index("{"):])
    return verdict
```

Binary criteria are easier to validate against human labels than 1–10 scores.

---

## Frequently Asked Questions

**How many eval cases do I need?**
Start with 20–50 covering your main scenarios and known failures. Grow to hundreds as the product matures. Larger sets are needed to detect small differences reliably.

**Can I use AI to generate eval cases?**
Yes, to expand coverage — but review them, mix them with real data, and don't let them replace real production samples.

**Should the judge model be the same as the production model?**
Preferably a different or stronger model, to reduce self-preference bias. Either way, validate against human labels.

**How do I evaluate agents?**
Evaluate the final outcome (did the task succeed, checked programmatically where possible — e.g., tests pass, the right record changed) and the trajectory (number of steps, cost, unnecessary or unsafe tool calls). Run tasks in reproducible sandboxed environments.

---

## Interview Questions

### Beginner

**Q1: Why can't you test an LLM feature with ordinary unit tests alone?**

*Model answer:* Outputs are nondeterministic, often have many acceptable forms, and a prompt or model change can affect behavior across all inputs. Unit tests still cover the deterministic code around the model — parsing, validation, tools — but model behavior needs evaluation over a dataset with graders, reported as success rates.

### Intermediate

**Q2: How would you evaluate a RAG-based question-answering system?**

*Model answer:* Separately at each stage. For retrieval: a labeled set of questions with the relevant source chunks, measuring recall@k. For generation: answer correctness, faithfulness to retrieved sources, citation accuracy, and correct "not found" behavior when no relevant source exists — using programmatic checks where possible and a validated LLM judge for the rest. Plus latency and cost, segmented by question type.

### Senior

**Q3: How do you decide whether to upgrade to a new model version?**

*Model answer:* Run the full eval suite on both versions with the same prompts, then adapt prompts if needed and re-run. Compare per-segment quality, format validity, safety cases, latency, and cost. Read a sample of differing outputs. If it passes the gates, roll out with a canary or shadow deployment, monitor online quality signals, and keep a fast rollback path.

### Architecture / Leadership

**Q4: How would you build an evaluation culture across multiple AI product teams?**

*Model answer:* Provide shared infrastructure — an eval harness, dataset storage, judge templates, CI integration, and dashboards — so evals are cheap to adopt. Require eval results for prompt and model changes in the same way we require tests for code. Make "every production AI bug becomes an eval case" a norm, review eval coverage in design reviews, and track quality metrics per segment next to reliability SLOs.

---

## Key Takeaways

1. Evals are the test suites of AI systems: a dataset of cases plus graders, reported as success rates.
2. Prefer programmatic graders; use LLM judges for open-ended quality only after validating them against humans.
3. Build datasets from real inputs, past failures, and deliberate edge cases — start small and grow.
4. Segment your metrics; averages hide the regressions that matter most.
5. Read raw failures regularly — they reveal patterns metrics can't.
6. Run evals in CI and gate prompt, retrieval, and model changes on them.
7. Combine offline evals with online monitoring, and turn production failures into new eval cases.

---

## Further Reading

- **"Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023)** — Zheng et al.: [https://arxiv.org/abs/2306.05685](https://arxiv.org/abs/2306.05685)
- **"Holistic Evaluation of Language Models (HELM)" (2022)** — Liang et al., Stanford CRFM: [https://arxiv.org/abs/2211.09110](https://arxiv.org/abs/2211.09110)
- **"SWE-bench" (2023)** — Jimenez et al.: [https://arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770)
- **Hamel Husain — "Your AI Product Needs Evals"**: [https://hamel.dev/blog/posts/evals/](https://hamel.dev/blog/posts/evals/)
- **"Site Reliability Engineering" (Google)** — the SLO and canary-release chapters translate directly to AI quality gates: [https://sre.google/books/](https://sre.google/books/)

---

*This chapter is part of the Modern Software Engineering Handbook — a comprehensive guide to the concepts, principles, and practices that every professional software engineer should know.*
