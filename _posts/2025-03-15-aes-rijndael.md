---
title: "AES: the primitive and the system around it"
description: "Why choosing AES is only one part of a confidentiality design: modes, keys, nonces and implementation matter."
date: 2025-03-15
modified: 2026-08-31
lang: en
topic: cryptography
guide_url: https://kmanu225.gitbook.io/cs/cryptography/aes-rijndael
tags:
  - cryptography
redirect_from:
  - /blog-post-1/
---

## The security question

AES provides a symmetric block-cipher primitive. A complete protection scheme also needs an appropriate mode of operation, sound key management and correct implementation.

The useful engineering question is not simply “are we using AES?” It is “what security property does the complete construction provide, and under which assumptions?”

## What to look at

- Distinguish confidentiality from integrity and authentication.
- Review how keys are generated, stored, used and replaced.
- Check the requirements of the selected mode, including nonce or initialization-vector handling.
- Prefer established implementations over custom cryptographic code.

## Practical perspective

An algorithm name on an architecture diagram is not evidence of end-to-end security. Protocol composition and lifecycle behavior are part of the review.

My longer note introduces AES and its role in protecting information. It is explanatory material, not a claim that a particular implementation has been audited.
