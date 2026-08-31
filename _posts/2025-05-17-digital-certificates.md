---
title: "Digital certificates: identity, keys and trust"
description: "Understanding what a certificate binds together, how a trust chain is validated, and what certificates do not guarantee."
date: 2025-05-17
modified: 2026-08-31
lang: en
topic: cryptography
guide_url: https://kmanu225.gitbook.io/cs/cryptography/pki/pki-digital-certificates
tags:
  - cryptography
redirect_from:
  - /blog-post-4/
---

A digital certificate associates a public key with identity information under an issuer's signature. The receiving application validates it against its own trust configuration.

Validation includes the expected service identity, validity period, permitted usages and issuer chain. A valid certificate does not establish that a service is harmless or that its private key is well protected.

The guide below explains these components. The [private PKI lab]({{ '/portfolio/2026-08-30-private-pki-lab/' | relative_url }}) shows a certificate authority and client configuration.
