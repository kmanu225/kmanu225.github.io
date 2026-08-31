---
title: "Private PKI lab with Step-CA"
card_title: "Private PKI lab"
excerpt: "A personal lab for setting up Step-CA, issuing certificates with ACME and configuring a client service."
description: "A Debian-based Step-CA lab covering certificate issuance, service configuration and client integration."
collection: portfolio
date: 2026-08-30
lang: en
portfolio_categories:
  - cryptography
study_type: "Personal lab · PKI engineering"
featured: true
rank: 2
link: "https://kmanu225.gitbook.io/cs/cryptography/pki/pki-demo"
link_label: "Read the PKI guide on GitBook"
---

I wrote a guide to setting up a private certificate authority with Step-CA and connecting it to a client service. It uses separate Debian-based CA and client environments.

This is a personal learning lab, not a client deployment.

## Steps covered

1. Prepare the CA and client environments.
2. Initialize the private CA with Step-CA.
3. Configure a service account, file ownership and systemd service.
4. Enable ACME for automated certificate issuance.
5. Configure the client service to use the private trust chain.

The commands and configuration are in the GitBook guide linked below.

## Before using it in production

The lab does not cover a production HSM deployment. A production design would also need to address root and intermediate CA separation, issuer authorization, renewal, revocation, monitoring, backup and recovery.

When reproducing the lab, check that the client validates the expected service identity and trust chain, that private-key permissions are appropriate, and that renewal works. Also test what happens when a certificate expires or the issuer is unavailable.
