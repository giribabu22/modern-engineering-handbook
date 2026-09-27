# 09 — Security

> *Security is not a feature. It is a property of the entire system.*

This section covers the fundamentals of software security from first principles. Rather than a checklist of vulnerabilities, you will learn the *mindset* of security — how attackers think, why systems are insecure by default, and how to build defense in depth — along with the practical fixes for the attacks you will actually face.

Start with **Why Hackers Succeed** — it explains the attacker's advantage and the common entry points the other chapters defend against.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [Why Hackers Succeed](Why-Hackers-Succeed.md) | ✅ Complete | 10 minutes |
| 2 | [The Most Common Web Attacks](The-Most-Common-Web-Attacks.md) | ✅ Complete | 10 minutes |
| 3 | [Zero Trust Architecture](Zero-Trust-Architecture.md) | ✅ Complete | 10 minutes |
| 4 | [How Secure Systems Are Built](How-Secure-Systems-Are-Built.md) | ✅ Complete | 10 minutes |
| 5 | [Cryptography for Engineers](Cryptography-For-Engineers.md) | ✅ Complete | 10 minutes |
| 6 | [Software Supply Chain Security](Software-Supply-Chain-Security.md) | ✅ Complete | 10 minutes |
| — | [Securing AI Systems](../15-AI-Era-Engineering/Securing-AI-Systems.md) *(in Section 15)* | ✅ Complete | 15 minutes |

## Key Ideas

- **Security is a mindset, not a checklist**: Attackers think in terms of "what can I make this system do that it wasn't designed to do?"
- **Attackers need one way in**: Reduce attack surface and fix the common entry points — credentials, phishing, unpatched software, misconfiguration, third parties.
- **Defense in depth**: No single security measure is sufficient. Layers of defense mean that breaking one doesn't break the system.
- **Separate data from code; never trust the client**: The two root causes behind most web vulnerabilities.
- **Never trust, always verify**: Zero trust replaces network location with identity, device, and least privilege.
- **Use the right cryptographic tool**: Most crypto bugs are the wrong primitive or a mishandled key, not broken math.
- **You ship other people's code**: Supply chain security protects dependencies, builds, and artifacts.
- **Any text a model reads is a potential instruction** *(AI era)*: Prompt injection has no complete fix; limit what a manipulated model can do.
- **Least privilege applies to agents** *(AI era)*: An AI agent should have exactly the permissions its task needs.

## Prerequisites

How The Internet Works (Section 03) recommended for context on network-level attacks.
