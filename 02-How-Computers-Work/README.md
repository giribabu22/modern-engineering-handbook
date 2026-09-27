# 02 — How Computers Work

> *Software runs on hardware. Understanding the hardware makes you a better engineer.*

This section demystifies what happens inside the machine when your code runs. You don't need to be a hardware engineer — but understanding the fundamentals of memory, CPUs, and operating systems will inform every performance decision you make. It also explains why AI runs on GPUs, why model size is measured in gigabytes of memory, and how operating systems keep AI agents contained.

## Chapters

| # | Chapter | Status | Est. Reading Time |
|---|---------|--------|-------------------|
| 1 | [What Happens When You Press A Key](What-Happens-When-You-Press-A-Key.md) | ✅ Complete | 35 minutes |
| 2 | [How Memory Works](How-Memory-Works.md) | ✅ Complete | 45 minutes |
| 3 | [How CPUs Execute Instructions](How-CPUs-Execute-Instructions.md) | ✅ Complete | 40 minutes |
| 4 | [How Operating Systems Work](How-Operating-Systems-Work.md) | ✅ Complete | 50 minutes |
| 5 | [The Memory Hierarchy: Registers, Cache, RAM, Disk](The-Memory-Hierarchy-Explained.md) | ✅ Complete | 40 minutes |
| 6 | How GPUs and AI Accelerators Work | 📝 Planned | — |

## Key Ideas

- **The latency gap**: CPU registers are 10 million times faster than disk. Everything in computer architecture is about bridging this gap.
- **Caching**: The most important performance technique in computing.
- **The operating system**: A resource manager that gives every program the illusion of having the whole machine to itself.
- **Moving data costs more than computing on it** *(AI era)*: LLM inference is usually limited by memory bandwidth, and the fastest AI kernels are designed around the memory hierarchy.
- **Isolation is a safety feature** *(AI era)*: Processes, permissions, and containers are how you let AI agents run commands without handing them the whole machine.

## Prerequisites

Basic programming experience recommended but not required.
