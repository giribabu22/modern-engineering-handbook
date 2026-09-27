# How Secure Systems Are Built

*Security isn't a final review. It's a set of habits woven through design, code, dependencies, deployment, and operations.*

---

> *“Every program and every user of the system should operate using the least set of privileges necessary to complete the job.”*
>
> — **Jerome Saltzer and Michael Schroeder**, "The Protection of Information in Computer Systems," 1975

## At a Glance

> **In one sentence:** Secure systems come from a secure development lifecycle — threat modeling during design, secure defaults and least privilege, safe coding patterns, automated scanning of code, secrets, and dependencies, hardened deployment, managed secrets, logging and detection, and a practiced response — so that security is built in rather than bolted on.

**You'll learn**

- Timeless design principles from Saltzer and Schroeder
- The secure development lifecycle, stage by stage
- Secrets management and why secrets leak
- Automated security testing: SAST, DAST, SCA, secret scanning
- Hardening infrastructure and the cloud
- Security logging, detection, vulnerability management, and response

**Before you start:** [Why Hackers Succeed](Why-Hackers-Succeed.md) · [The Most Common Web Attacks](The-Most-Common-Web-Attacks.md)

**Reading time:** about 10 minutes

---

## The Big Picture

```mermaid
flowchart LR
    D["Design<br/>threat model,<br/>security requirements"] --> C["Code<br/>safe patterns,<br/>review"]
    C --> CI["CI<br/>SAST, dependency scan,<br/>secret scan, tests"]
    CI --> B["Build<br/>signed artifacts,<br/>minimal images"]
    B --> DEP["Deploy<br/>hardened config,<br/>least privilege, secrets manager"]
    DEP --> OPS["Operate<br/>logging, detection,<br/>patching, pentests"]
    OPS --> IR["Respond<br/>incident response,<br/>postmortems"]
    IR -. "lessons" .-> D
```

*Security activities at every stage — each one cheaper than fixing the same problem after a breach.*

---

## Introduction

A startup builds its product fast. Security is "something to do before the big enterprise deal." When that deal arrives, the customer's security questionnaire asks about threat modeling, dependency scanning, secrets management, encryption, audit logging, and incident response. The answer to most questions is "not yet." Retrofitting takes six months — rewriting authorization, rotating hundreds of hard-coded credentials, and adding logs that should have existed from the start.

A second startup takes a different approach from day one: a one-page threat model for each major feature, secrets in a secrets manager, CI that blocks commits containing keys, dependency updates automated weekly, and a framework with safe defaults. None of it slowed them down much. When the enterprise questionnaire arrives, most answers are "yes, here's how."

The difference is **when** security happens. Built in early, it's mostly habits and tooling. Bolted on late, it's an expensive rewrite.

### Why Should Engineers Care?

- Most vulnerabilities are introduced during everyday development — and are cheapest to fix there.
- Customers, regulators, and partners increasingly require evidence of secure development practices.
- Good security tooling mostly runs automatically, protecting you without constant effort.

---

## The Problem It Solves

| Without a secure lifecycle | With one |
|---------------------------|---------|
| Security reviewed once, before launch (if at all) | Security considered at every stage |
| Vulnerabilities found by attackers or customers | Found by threat models, scanners, and tests |
| Secrets in code, configs, chat | Secrets in a manager, rotated, scanned for |
| Outdated dependencies | Automated updates and vulnerability alerts |
| No audit trail | Security logging and detection |
| Improvised breach response | Practiced incident response |

---

## Historical Background

- **1975 — Saltzer and Schroeder** published eight design principles for protection — including least privilege, fail-safe defaults, economy of mechanism, and complete mediation — that remain the foundation of secure design.
- **2002 — Microsoft's Trustworthy Computing memo** from Bill Gates made security a company priority; Microsoft's Security Development Lifecycle (SDL) followed and became an industry model.
- **2000s — OWASP** projects (Top 10, ASVS, cheat sheets) gave developers practical, free guidance.
- **2010s — DevSecOps** integrated security scanning into CI/CD pipelines; bug bounty programs became common.
- **2011 onward — Automated dependency and secret scanning** tools spread, later built into code hosting platforms.
- **2021–2022 — Secure software development frameworks,** such as NIST's Secure Software Development Framework (SSDF, SP 800-218), became expectations for software suppliers, especially to governments.

---

## Core Concepts

### Saltzer and Schroeder's Principles (Selected)

| Principle | Meaning today |
|----------|--------------|
| **Least privilege** | Minimal permissions for users, services, and tokens |
| **Fail-safe defaults** | Deny by default; access must be granted explicitly |
| **Economy of mechanism** | Keep security-critical code small and simple |
| **Complete mediation** | Check authorization on every access, not just the first |
| **Open design** | Security must not depend on keeping the design secret |
| **Separation of privilege** | Require more than one condition (for example, MFA, two-person approval) |
| **Least common mechanism** | Minimize shared components that could leak between users |
| **Psychological acceptability** | Secure behavior must be easy, or people will work around it |

### The Secure Development Lifecycle

1. **Requirements:** what data is sensitive? What regulations apply? Who are the users and attackers?
2. **Design:** threat model (STRIDE), choose authentication and authorization models, plan encryption and logging.
3. **Implementation:** safe frameworks, input validation, parameterized queries, output encoding, code review with a security lens.
4. **Verification:** static analysis (SAST), dependency scanning (SCA), secret scanning, dynamic scanning (DAST), security tests (for example, authorization tests), penetration testing.
5. **Release:** signed artifacts, minimal container images, hardened configuration, least-privilege deployment roles.
6. **Operations:** patching, vulnerability management, logging and detection, access reviews.
7. **Response:** incident response plans, postmortems, disclosure processes.

### Secrets Management

Secrets — API keys, database passwords, signing keys, tokens — leak through source code, configuration files, container images, logs, CI output, tickets, and chat. Good practice:

- Store secrets in a **secrets manager** (cloud secret stores, HashiCorp Vault, and similar).
- Prefer **short-lived, automatically issued credentials** (workload identity) over static secrets.
- **Rotate** regularly and immediately after exposure.
- **Scan** repositories and commits for secrets, and block pushes containing them.
- **Never log** secrets; redact tokens in error messages.

### Automated Security Testing

| Tool type | What it checks | When |
|----------|---------------|-----|
| SAST (static analysis) | Code patterns: injection, unsafe functions | Every pull request |
| SCA (software composition analysis) | Known-vulnerable dependencies and licenses | Every build + continuously |
| Secret scanning | Keys and passwords in code and history | Pre-commit, push, and CI |
| DAST (dynamic analysis) | Running app: XSS, misconfiguration, headers | Staging environments |
| IaC scanning | Terraform/Kubernetes misconfigurations | Every change to infrastructure code |
| Container image scanning | Vulnerable OS packages in images | Build and registry |

### Hardening

- **Minimal images and hosts:** fewer packages, fewer vulnerabilities.
- **Private by default:** storage buckets, databases, and admin interfaces not public.
- **Least-privilege IAM** for every service and pipeline.
- **Encryption** in transit (TLS everywhere) and at rest.
- **Secure configuration baselines** (for example, CIS Benchmarks).

### Vulnerability Management

Track, prioritize, and fix vulnerabilities with defined timelines — prioritizing by exploitability and exposure (internet-facing, known exploited) rather than raw severity scores alone.

### Security Logging and Detection

Log authentication events, authorization failures, admin actions, data exports, and configuration changes — centrally, tamper-resistantly, with alerts for suspicious patterns.

---

## Real-World Analogy

### Building Codes for Software

Buildings are safe not because an inspector looks at them once at the end, but because codes shape every stage: fire-resistant materials chosen at design, wiring done to standard, inspections at key milestones, smoke detectors installed, and evacuation drills held regularly. A secure development lifecycle is software's building code — and like building codes, most of it is routine once it's habit.

---

## How It Works In Practice

### A Security-Aware Pull Request

- The PR description notes any new data flows, endpoints, or permissions.
- CI runs unit tests, SAST, dependency scanning, and secret scanning; any critical finding blocks the merge.
- The reviewer checks authorization on new endpoints, input handling, logging of sensitive data, and error messages.
- Infrastructure changes are scanned for public exposure and overly broad permissions.

### A Lightweight Threat Model Template

```
Feature:           Export account data as CSV
Assets:            Personal data of the account's users
Entry points:      POST /exports, GET /exports/{id}/download
Trust boundaries:  Browser → API → export worker → object storage
Threats (STRIDE):  IDOR on download; export of other tenants' data; CSV formula injection;
                   large exports as DoS; download links shared publicly
Mitigations:       Ownership check; tenant filter in query; escape leading = + - @ in cells;
                   rate limits + size caps; short-lived signed URLs; audit log of exports
Residual risk:     Users may forward downloaded files — accepted, documented
```

### Vulnerability Response Timelines (example policy)

| Severity and exposure | Fix within |
|----------------------|-----------|
| Known exploited, internet-facing | 48 hours |
| Critical | 7 days |
| High | 30 days |
| Medium | 90 days |

---

## Production Engineering Perspective

- **Automate the boring parts:** dependency update bots, CI scanners, and policy checks catch most issues without human effort.
- **Tune scanners** so findings are trusted; floods of false positives get ignored.
- **Security champions** in each team spread practices better than a central team reviewing everything.
- **Penetration tests and bug bounties** find what automation misses, especially business-logic flaws.
- **Evidence matters:** customers and auditors (for example, for SOC 2 or ISO 27001) ask for proof of practices, so keep records of reviews, scans, and access reviews.

---

## Tradeoffs

| Practice | Benefit | Cost |
|---------|--------|-----|
| Blocking CI on findings | Stops vulnerable code shipping | Friction; needs tuned rules |
| Threat modeling every feature | Early detection of design flaws | Time; must stay lightweight |
| Frequent dependency updates | Fewer known vulnerabilities | Breakage risk; testing effort |
| Strict least privilege | Small blast radius | Access requests and admin overhead |
| Bug bounty | External expertise at scale | Triage load; payouts |

---

## Common Mistakes

### Beginner Mistakes

- Secrets in source code or `.env` files committed to Git.
- Default-allow permissions ("give it admin, we'll tighten later").
- Logging full request bodies, including passwords and tokens.

### Intermediate Mistakes

- Scanners installed but findings never fixed.
- Rotating a leaked secret in one place but not everywhere it was copied.
- Security review only at launch, never for later changes.

### Senior-Level Mistakes

- No ownership of vulnerability management across teams.
- Treating compliance checklists as equivalent to security.
- Security controls so painful that engineers routinely bypass them.

---

## Failure Scenarios

### Scenario 1: The Secret in Git History

A key was committed, then removed in the next commit. It still exists in the repository history — and in every clone.

**Mitigation:** treat any committed secret as compromised: rotate it immediately; use pre-commit and push-time secret scanning.

### Scenario 2: The Public Bucket

A storage bucket is made public for a quick file share and forgotten. It later contains customer exports.

**Mitigation:** block public access by default at the account level; IaC scanning; alerts on policy changes.

### Scenario 3: The Ignored Scanner

The dependency scanner reports hundreds of issues; the team stops looking. A critical, exploited vulnerability is among them.

**Mitigation:** prioritize by exploitability and exposure, fix the backlog incrementally, block new critical issues.

### Scenario 4: The Overpowered CI Pipeline

The CI system has production admin credentials. A malicious pull request from a fork runs a workflow that exfiltrates them.

**Mitigation:** least-privilege, short-lived deployment credentials; no secrets for untrusted forks; protected branches and environments.

---

## Real-World Industry Examples

- **Microsoft's Security Development Lifecycle** is a long-standing public model of secure development practices.
- **NIST SSDF (SP 800-218)** describes secure software development practices expected of software suppliers.
- **GitHub, GitLab, and other platforms** offer built-in secret scanning, dependency alerts, and code scanning.
- **OWASP SAMM** (Software Assurance Maturity Model) helps organizations assess and improve their security practices.

---

## Interview Questions

### Beginner

**Q1: Where should application secrets be stored?**

*Model answer:* In a secrets manager (or provided through short-lived workload identity), injected at runtime, with access limited by least privilege — never in source code, configuration files in Git, images, or logs.

### Intermediate

**Q2: What's the difference between SAST, DAST, and SCA?**

*Model answer:* SAST analyzes source code for insecure patterns without running it. DAST tests a running application from the outside for vulnerabilities like XSS or misconfiguration. SCA checks third-party dependencies for known vulnerabilities and license issues.

**Q3: A secret was committed and pushed. What do you do?**

*Model answer:* Treat it as compromised: revoke and rotate it immediately, check logs for misuse, update every place that used it, then clean it from history if appropriate — but rotation, not history rewriting, is the real fix. Add secret scanning to prevent recurrence.

### Senior

**Q4: How would you prioritize a backlog of 2,000 vulnerability findings?**

*Model answer:* Focus on exploitability and exposure: known-exploited vulnerabilities and internet-facing systems first, then critical issues reachable by attackers, deprioritizing unreachable code paths. Fix by upgrading the few dependencies behind many findings, block new critical findings in CI, and set SLAs per severity.

### Architecture / Leadership

**Q5: How would you introduce a secure development lifecycle into a fast-moving product organization?**

*Model answer:* Start with automated controls that add little friction: secret scanning, dependency updates, SAST on pull requests, safe framework defaults. Add lightweight threat modeling for new features and a security checklist in design reviews. Train security champions in each team, set vulnerability SLAs, add security logging, run periodic penetration tests, and practice incident response. Measure findings over time and keep controls tuned so they're trusted.

---

## Hands-On Lab

Build a small secret scanner like the ones that run in CI. Pure Python; save as `secret_scan_lab.py` and run it.

```python
import math, re

files = {
    "config.py": 'DEBUG = True\nAWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"\nREGION = "ap-south-1"\n',
    # the fake key is split in two so that real secret scanners don't flag this example
    "app.js": 'const stripe = require("stripe")("sk_' + 'live_4eC39HqLyjWDarjtT1zdp7dc");\n',
    "notes.md": "Deploy steps: run make deploy. Ping Sam if it fails.\n",
    "settings.yaml": "db_password: hunter2\napi_token: 9f8e7d6c5b4a39281706f5e4d3c2b1a0\n",
    "README.md": "Use your own API key in the .env file (never commit it).\n",
}

PATTERNS = {
    "AWS access key ID": r"AKIA[0-9A-Z]{16}",
    "Stripe live secret key": r"sk_live_[0-9a-zA-Z]{24,}",
    "Password assignment": r"(?i)(password|passwd|pwd)\s*[:=]\s*(\S+)",
    "Generic token assignment": r"(?i)(token|secret|api_key)\s*[:=]\s*['\"]?([A-Za-z0-9/+_-]{16,})",
}

def entropy(s):
    """Shannon entropy in bits per character: random strings score high."""
    return -sum(s.count(c) / len(s) * math.log2(s.count(c) / len(s)) for c in set(s))

findings = []
for name, text in files.items():
    for line_no, line in enumerate(text.splitlines(), 1):
        for rule, pattern in PATTERNS.items():
            for m in re.finditer(pattern, line):
                value = m.group(m.lastindex or 0)
                findings.append((name, line_no, rule, value[:4] + "...", round(entropy(value), 1)))

for f in findings:
    print(f"{f[0]:14} line {f[1]}  {f[2]:26} value={f[3]:8} entropy={f[4]}")
print(f"\n{len(findings)} finding(s): block the commit, rotate every real secret found.")
```

(The AWS key above is Amazon's documented example key, and the Stripe key is a fake — neither is real. The fake key is split in the source so that real scanners, like the one protecting this repository, don't flag the example.)

**What to notice**
- Specific patterns (like `AKIA…` for AWS access key IDs, `sk_live_` for Stripe) catch well-known secret formats precisely.
- Generic rules (`password: …`, `token = …`) catch more, but produce false positives; entropy helps distinguish random secrets from ordinary words.
- The README mentioning "API key" isn't flagged — good rules look for assignments of values, not words.
- Real scanners (built into code platforms, or open-source tools like gitleaks and truffleHog) use hundreds of rules, scan full history, and can verify whether a found key is live.

---

## Test Yourself

*Answer each question in your head or on paper first, then open the answer to check.*

<details markdown="1">
<summary><strong>1. What does "fail-safe defaults" mean?</strong></summary>

Access is denied unless explicitly granted, so mistakes and omissions result in denial rather than exposure.

</details>

<details markdown="1">
<summary><strong>2. What does "complete mediation" require?</strong></summary>

Checking authorization on every access to every object — not caching a decision from the first access and trusting it forever.

</details>

<details markdown="1">
<summary><strong>3. Why isn't deleting a committed secret in a later commit enough?</strong></summary>

It remains in the repository history and every existing clone. The secret must be rotated.

</details>

<details markdown="1">
<summary><strong>4. What does SCA check?</strong></summary>

Third-party dependencies for known vulnerabilities (and license issues).

</details>

<details markdown="1">
<summary><strong>5. How should vulnerabilities be prioritized?</strong></summary>

By exploitability and exposure — known-exploited and internet-facing first — not by severity score alone.

</details>

<details markdown="1">
<summary><strong>6. What is "psychological acceptability" in secure design?</strong></summary>

Security mechanisms must be easy enough to use that people follow them rather than working around them.

</details>

<details markdown="1">
<summary><strong>7. Name three things that should be security-logged.</strong></summary>

Any three of: authentication events, authorization failures, admin actions, data exports, permission and configuration changes.

</details>

---

## Cheat Sheet

**Principles:** least privilege · fail-safe defaults · economy of mechanism · complete mediation · open design · separation of privilege · psychological acceptability.

| Stage | Key practices |
|------|--------------|
| Design | Threat model, security requirements, data classification |
| Code | Safe frameworks, validation, encoding, parameterized queries, security-minded review |
| CI | SAST, SCA, secret scanning, IaC scanning, security tests |
| Build | Minimal images, signed artifacts |
| Deploy | Secrets manager, least-privilege IAM, private-by-default, encryption |
| Operate | Patching SLAs, logging and detection, access reviews, pentests, bug bounty |
| Respond | Incident response plan, rotation playbooks, postmortems |

**Leaked secret playbook:** revoke/rotate → check for misuse → update all consumers → scan to prevent recurrence.

---

## In the AI Era

- **AI speeds up code — and vulnerabilities.** Keep automated scanning and review in the loop for AI-generated changes; assistants can introduce injection, missing authorization, and hard-coded secrets.
- **Secrets and AI tools:** don't paste secrets into AI chats; coding agents should run without access to production secrets.
- **Threat model AI features** as part of design: prompt injection, data leakage, tool permissions, and model-provider data handling. See [Securing AI Systems](../15-AI-Era-Engineering/Securing-AI-Systems.md).
- **AI as a security reviewer** can find issues and explain fixes, useful as a first pass alongside SAST and human review.

**Try it:** Add a rule to the lab that detects a pattern of your choice (for example, a model provider API key prefix you know). Test it on a fake example.

---

## Key Takeaways

1. Build security into every stage of development — it's far cheaper than retrofitting.
2. Saltzer and Schroeder's principles (least privilege, fail-safe defaults, complete mediation) still guide secure design.
3. Keep secrets in a manager, prefer short-lived credentials, scan for leaks, and rotate on exposure.
4. Automate security testing in CI: SAST, SCA, secret scanning, IaC scanning.
5. Harden deployments: private by default, least-privilege IAM, encryption, minimal images.
6. Manage vulnerabilities by exploitability and exposure, and practice incident response.

---

## What to Read Next

- **[Cryptography for Engineers](Cryptography-For-Engineers.md)** — using cryptographic primitives correctly
- **[Software Supply Chain Security](Software-Supply-Chain-Security.md)** — securing the code you didn't write
- **[Deployments: Strategies and Risks](../11-Production-Engineering/Deployments-Strategies-And-Risks.md)** — where security checks fit in the pipeline

---

## Further Reading

- **Saltzer & Schroeder — "The Protection of Information in Computer Systems" (1975):** [https://www.cs.virginia.edu/~evans/cs551/saltzer/](https://www.cs.virginia.edu/~evans/cs551/saltzer/)
- **NIST SP 800-218 — Secure Software Development Framework:** [https://csrc.nist.gov/projects/ssdf](https://csrc.nist.gov/projects/ssdf)
- **Microsoft Security Development Lifecycle:** [https://www.microsoft.com/en-us/securityengineering/sdl](https://www.microsoft.com/en-us/securityengineering/sdl)
- **OWASP SAMM:** [https://owaspsamm.org](https://owaspsamm.org)
- **Google — "Building Secure and Reliable Systems" (2020), free online:** [https://sre.google/books/](https://sre.google/books/)
- **CIS Benchmarks:** [https://www.cisecurity.org/cis-benchmarks](https://www.cisecurity.org/cis-benchmarks)

---

*This chapter is part of the Modern Software Engineering Handbook — a comprehensive guide to the concepts, principles, and practices that every professional software engineer should know.*
