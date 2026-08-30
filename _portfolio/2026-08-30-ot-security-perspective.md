---
title: "Industrial and embedded security: an audit perspective"
card_title: "OT/IoT security perspective"
excerpt: "Connecting risk analysis, equipment security and cryptographic dependencies in electricity-distribution environments."
description: "A non-confidential overview of Emmanuel Konan’s industrial and embedded security experience and audit perspective."
collection: portfolio
date: 2026-08-30
lang: en
category: security
study_type: "Professional experience · Methodology"
rank: 3
---

## Context and experience

My experience at Enedis and Ornisec includes cybersecurity work on industrial and embedded equipment for electricity distribution. The scope described in my CV covers risk analysis, equipment security specifications, qualification, auditing and inventory/mapping.

This page is a **non-confidential professional perspective**, not an anonymized account of a specific client engagement. It contains no internal architecture, client finding or claimed remediation result.

## My areas of contribution

- EBIOS-RM risk analysis and defense-in-depth approaches.
- Security work involving PKI, HSMs, PKCS#11 and embedded equipment.
- Technical audit topics spanning architecture, configuration and source code.
- Earlier work-study experience involving PCB testing and Python/Bash scripting.

## A practical review sequence

The following is a general way to frame the work, rather than a reconstruction of any client’s audit:

1. **Understand the function.** Identify the equipment’s purpose, dependencies, operational constraints and impact of failure.
2. **Map the trust boundaries.** Separate interfaces, privileged operations, update paths and cryptographic dependencies.
3. **Relate threats to controls.** Connect the risk analysis to specific architecture and implementation questions.
4. **Examine lifecycle behavior.** Include provisioning, maintenance, recovery and decommissioning.
5. **Make recommendations actionable.** Distinguish the observation, evidence, consequence and proposed remediation.

## Where cryptography enters the picture

Authentication and key management cross hardware, firmware and backend boundaries. A review must ask where keys originate, where they are stored, what operations may use them and how credentials are replaced.

This makes cryptographic infrastructure part of the operational architecture, not a separate mathematical layer.

## What can be shared

Public protocol contributions and personal learning material are linked elsewhere on this site. Mission-specific scope, detailed responsibilities and outcomes can only be discussed to the extent permitted by confidentiality obligations.
