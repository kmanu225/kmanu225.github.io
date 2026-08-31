---
title: "Auditing industrial and embedded systems"
card_title: "OT/IoT security audits"
excerpt: "My work on equipment security and risk analysis in electricity distribution."
description: "The questions I use to structure reviews of industrial equipment, authentication and key management."
collection: portfolio
date: 2026-08-30
lang: en
portfolio_categories:
  - security-audits
  - industrial-systems
study_type: "Professional experience · Methodology"
rank: 3
---

At Enedis and Ornisec, I have worked on cybersecurity for industrial and embedded equipment used in electricity distribution. My tasks have included risk analysis, security specifications, qualification, audits and equipment inventory.

This page describes my general approach. It does not document a specific client audit or disclose internal findings.

## Audit questions

1. What does the equipment do, and what would a failure affect?
2. Which interfaces, privileged operations and update paths need review?
3. How do the identified risks relate to the architecture and configuration?
4. How is the equipment provisioned, maintained, recovered and retired?
5. What evidence supports each finding and proposed remediation?

## Authentication and keys

Reviews involving PKI, HSMs or PKCS#11 include checking where keys are generated and stored, who can use them and how credentials are replaced. These questions span the equipment, firmware and backend services.

My [CV]({{ '/cv/' | relative_url }}) lists the roles and associated responsibilities.
