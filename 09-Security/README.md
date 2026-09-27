# 09 — Security

> *Security is not a feature. It is a property of the entire system.*

This section covers the fundamentals of software security from first principles. Rather than a checklist of vulnerabilities, you will learn the *mindset* of security — how attackers think, why systems are insecure by default, and how to build defense in depth.

## Chapters

| # | Chapter | Status |
|---|---------|--------|
| 1 | Why Hackers Succeed | 📝 Planned |
| 2 | The Most Common Web Attacks | 📝 Planned |
| 3 | Zero Trust Architecture | 📝 Planned |
| 4 | How Secure Systems Are Built | 📝 Planned |
| 5 | Cryptography for Engineers | 📝 Planned |
| 6 | Software Supply Chain Security | 📝 Planned |
| — | [Securing AI Systems](../15-AI-Era-Engineering/Securing-AI-Systems.md) *(in Section 15)* | ✅ Complete |

## Key Ideas

- **Security is a mindset, not a checklist**: Attackers think in terms of "what can I make this system do that it wasn't designed to do?"
- **Defense in depth**: No single security measure is sufficient. Layers of defense mean that breaking one doesn't break the system.
- **The weakest link is always human**: The most secure encryption is useless if someone shares their password.
- **Any text a model reads is a potential instruction** *(AI era)*: Prompt injection has no complete fix; limit what a manipulated model can do.
- **Least privilege applies to agents** *(AI era)*: An AI agent should have exactly the permissions its task needs — and nothing that can't be undone without a human's approval.

## Prerequisites

How The Internet Works (Section 03) recommended for context on network-level attacks.
