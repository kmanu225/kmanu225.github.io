---
title: "Elliptic-curve cryptography: the mathematical foundation"
description: "An introduction to elliptic curves and the distinction between mathematical structure and secure protocol implementation."
date: 2025-04-15
modified: 2026-08-31
lang: en
topic: cryptography
guide_url: https://kmanu225.gitbook.io/cs/cryptography/elliptic-curve-cryptography/part-1-what-are-elliptic-curves
tags:
  - cryptography
redirect_from:
  - /blog-post-2/
---

This first part of my elliptic-curve series introduces the mathematical objects and geometric intuition. The second part moves to finite fields.

Elliptic-curve cryptography uses mathematical structures where some operations are efficient but the corresponding inverse problems are computationally difficult. This allows relatively compact public keys. Comparisons with RSA need to use equivalent security levels, not equal key lengths.

The guide focuses on the mathematics. Implementations also need appropriate parameters, input validation and protection against side channels.
