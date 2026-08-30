---
title: "DoctorPDF: local document processing and release engineering"
card_title: "DoctorPDF"
excerpt: "A desktop PDF tool with local processing, machine-bound licensing and automated release workflows."
description: "DoctorPDF engineering case study: local processing, desktop distribution and explicit boundaries around privacy and security claims."
collection: portfolio
date: 2026-08-12
lang: en
category: security
study_type: "Software project · Desktop engineering"
rank: 4
link: "https://github.com/kmanu225/DoctorPDF/releases"
link_label: "View public releases on GitHub"
---

## Context

DoctorPDF is a desktop application for common PDF operations: merging, compression, watermarking, redaction and password protection. Its processing model keeps document operations on the user’s machine instead of requiring a cloud upload.

## My contribution

I developed the application and its distribution workflow, including machine-fingerprint licensing, an activation screen and system-clock tamper checks.

The project includes Windows x64 and Debian/Linux distribution and GitHub Actions release automation.

## Engineering choices

- **Local document processing:** avoid making a cloud processing service a requirement for core PDF operations.
- **Desktop distribution:** package the application for users outside the development environment.
- **Machine-bound licensing:** associate licensing with a device fingerprint.
- **Release automation:** use CI/CD to make the build and publication workflow repeatable.

## Deliverable

A desktop application with public release artifacts. The release page is the reference for available versions and supported packages.

## Security boundaries

Local processing is a design choice, not a blanket privacy certification. Licensing and update behavior need to be considered separately from the document-processing path.

Redaction also needs independent verification: a visually covered area is not, by itself, evidence that the underlying text has been removed. Release signing, artifact integrity and tamper resistance should be verified against the actual release process.

This case study does not claim an independent audit, quantified privacy improvement or an unbreakable licensing mechanism.
