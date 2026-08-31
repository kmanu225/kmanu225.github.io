---
title: "HSMs: key storage and access"
description: "How hardware security modules protect keys, and the access and recovery decisions involved."
date: 2025-06-22
modified: 2026-08-31
lang: en
topic: cryptography
guide_url: https://kmanu225.gitbook.io/cs/cryptography/pki/pki-hsm
featured: true
rank: 2
tags:
  - cryptography
redirect_from:
  - /blog-post-6/
---

A hardware security module (HSM) stores keys and performs cryptographic operations within a dedicated hardware boundary.

Integration requires decisions about key access and recovery:

- Which keys are generated inside the HSM, imported or exportable?
- Which applications and operators can use them?
- How are privileged roles separated and their actions logged?
- How are keys backed up and recovered when hardware is replaced?

The guide below introduces HSMs in a PKI. The [PKCS#11 note]({{ '/pkcs11/' | relative_url }}) covers an interface used by applications to access cryptographic tokens.
