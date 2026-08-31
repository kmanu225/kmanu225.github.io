---
title: "Linux persistence mechanisms"
description: "Notes on detecting and removing persistence mechanisms after a Linux compromise."
date: 2025-08-24
modified: 2026-08-31
lang: en
topic: systems
guide_url: https://kmanu225.gitbook.io/cs/system/linux/security/persistence-mechanisms
tags:
  - systems
redirect_from:
  - /blog-post-9/
---

Persistence mechanisms let an attacker regain execution or access after a compromise. My note was prompted by [John Hammond’s Black Hat USA 2025 material](https://www.youtube.com/watch?v=whhOYRWd_rs) and covers prevention, detection and removal.

For each mechanism, the questions are: what executes, which privileges are needed, what traces remain and what causes it to run again?

Removing a suspicious startup entry is only part of recovery. The investigation also needs to establish the original compromise and which parts of the system can still be trusted. The guide is intended for authorized defensive learning and testing.
