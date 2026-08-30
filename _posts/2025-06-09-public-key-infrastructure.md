---
title: "PKI: operating a chain of trust"
description: "Certificates, certification authorities and lifecycle management as an operational security architecture."
date: 2025-06-09
modified: 2026-08-31
lang: en
topic: cryptography
guide_url: https://kmanu225.gitbook.io/cs/cryptography/pki/pki-foundation
tags:
  - cryptography
redirect_from:
  - /blog-post-5/
---

## Beyond certificate issuance

A public key infrastructure brings together technology, policy and operations around identities and public keys. Certification authorities issue credentials; relying parties decide which issuers and identities to trust.

## The architectural questions

- Which identities and use cases are in scope?
- Where are trust anchors distributed and maintained?
- How are CA keys protected?
- Who may request, approve, renew or revoke a certificate?
- How will the service recover from compromise or unavailability?

## Practical perspective

A PKI design should connect these decisions to operational ownership. Renewal, monitoring and recovery cannot be left until after certificate issuance works.

My foundational guide explains the components. The [private PKI lab]({{ '/portfolio/2026-08-30-private-pki-lab/' | relative_url }}) explores how they fit together in a learning environment, with production requirements treated separately.
