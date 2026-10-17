---
title: "Static compilation for a target with an old GLIBC"
description: "Building a self-contained binary when the target system's C library is too old to run a dynamically linked tool."
date: 2026-10-15
lang: en
topic: software-engineering
guide_url: https://kmanu225.gitbook.io/cs/software-engineering/compilation/fundamentals
tags:
  - software-engineering
---

An old exploit I wanted to fire against a target wouldn't run: its C library was too old (an early GLIBC) to satisfy the binary's dynamic dependencies. Building the exploit statically was the simplest fix, since the binary then carries everything it needs at runtime.

Static linking bundles the required library code into the binary itself. The result is larger and must match the target's architecture and ABI, but it no longer depends on the versions installed on the host, which makes it portable across older or minimal systems. The guide covers the compilation fundamentals and the trade-offs between static and dynamic linking.
