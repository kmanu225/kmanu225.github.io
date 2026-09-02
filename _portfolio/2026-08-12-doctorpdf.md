---
title: "DoctorPDF: a desktop PDF tool"
card_title: "DoctorPDF"
excerpt: "A desktop PDF tool with local processing, machine-bound licensing and automated release workflows."
description: "Development of DoctorPDF: local PDF processing, device licensing and Windows/Linux packaging."
collection: portfolio
date: 2026-08-12
lang: en
portfolio_categories:
  - software-engineering
study_type: "Software project · Desktop engineering"
rank: 4
link: "https://github.com/kmanu225/DoctorPDF/releases"
link_label: "View public releases on GitHub"
---

DoctorPDF is a desktop application I developed for merging, compressing, watermarking, redacting and password-protecting PDFs. Document processing runs on the user's machine.

## Development and distribution

I implemented machine-fingerprint licensing, an activation screen and system-clock tamper checks. I also set up Windows x64 and Debian/Linux packaging with GitHub Actions release automation.

Available packages and versions are listed on the release page below.

## Security considerations

Local document processing does not establish the privacy of licensing or update behavior. Those paths need separate review.

Redaction needs verification that the underlying text is removed, not just visually covered. Release signing, artifact integrity and licensing tamper resistance also need independent verification.
