---
title: "AES: modes, keys and implementation"
description: "An introduction to AES and the mode, key and nonce choices involved in using it."
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

AES is a symmetric block cipher. Using it in a system also requires a mode of operation, key management and correct implementation.

When reviewing its use, I look at:

- Whether the application needs confidentiality, integrity and authentication.
- How keys are generated, stored and replaced.
- The selected mode's requirements for nonces or initialization vectors.
- Which cryptographic library provides the implementation.

The guide below introduces the algorithm.
