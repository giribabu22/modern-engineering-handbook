# 03 — How The Internet Works

> *The internet is not a cloud. It is a collection of tubes, switches, and protocols that somehow still works.*

This section covers the fundamentals of networking — from the physical layer of fiber optic cables to the application layer protocols that power the web. Every software engineer should understand what happens between hitting "Enter" and seeing a page load — and, increasingly, what happens when an AI model streams an answer back over the same protocols.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [How The Internet Really Works](How-The-Internet-Really-Works.md) | ✅ Complete | 45 minutes |
| 2 | [How A Webpage Reaches Your Screen](How-A-Webpage-Reaches-Your-Screen.md) | ✅ Complete | 40 minutes |
| 3 | [How DNS Works](How-DNS-Works.md) | ✅ Complete | 30 minutes |
| 4 | [How HTTPS Protects Your Data](How-HTTPS-Protects-Your-Data.md) | ✅ Complete | 35 minutes |
| 5 | [HTTP, TCP/IP, and the Protocol Stack](HTTP-TCP-IP-and-the-Protocol-Stack.md) | ✅ Complete | 45 minutes |
| 6 | Streaming, WebSockets, and Long-Lived Connections | 📝 Planned | — |

## Key Ideas

- **Protocols are agreements**: The internet works because everyone agrees on the same rules for sending and receiving data.
- **Layered abstraction**: Each layer (physical → link → network → transport → application) handles one concern and hides the rest.
- **DNS is the phonebook of the internet**: Without it, we'd be memorizing IP addresses.
- **Encryption is not optional**: HTTPS is the baseline for any production service.
- **Streaming changes assumptions** *(AI era)*: LLM responses are long-lived streams that stress timeouts, proxies, and load balancers built for short requests.
- **Outbound requests are an attack surface** *(AI era)*: Agents that fetch URLs need SSRF protection, just like any server-side fetcher.

## Prerequisites

No networking background required. Curiosity about how the internet works is enough.
