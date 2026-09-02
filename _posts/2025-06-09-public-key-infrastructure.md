---
title: "PKI: certificate authorities and lifecycle management"
description: "Certificate issuance, trust anchors, renewal and recovery in a public key infrastructure."
date: 2025-06-09
modified: 2026-08-31
lang: en
topic: cryptography
guide_url: https://kmanu225.gitbook.io/cs/cryptography/pki/pki-foundations
tags:
  - cryptography
redirect_from:
  - /blog-post-5/
---

A public key infrastructure organizes certificate issuance and validation. Certification authorities issue certificates; applications use configured trust anchors to decide which issuers to accept.

Setting up a PKI involves deciding:

- Which identities and services it covers.
- How trust anchors are distributed.
- How CA keys are protected.
- Who can request, approve, renew or revoke certificates.
- How the service is monitored and recovered after a failure or compromise.

The guide introduces the components. The [private PKI lab]({{ '/portfolio/2026-08-30-private-pki-lab/' | relative_url }}) covers a small Step-CA setup.
