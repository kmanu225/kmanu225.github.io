---
title: "DoctorPDF — Local PDF Processing Suite"
excerpt: "Cross-platform desktop app for local PDF processing (merge, compress, watermark, redact, password-protect), with a machine-fingerprint licensing system and automated releases via GitHub Actions."
collection: portfolio
date: 2026-08-12
link: "https://github.com/kmanu225/DoctorPDF/releases"
---

DoctorPDF is a desktop application for processing PDF documents entirely on the user's machine, with no files ever leaving the device.

**Features**
- Merge, compress, watermark, redact, and password-protect PDFs
- 100% local processing — no cloud upload, no third-party servers
- Machine-fingerprint licensing with an activation screen
- System-clock tamper detection to prevent date-based license bypass
- Cross-platform: Windows (x64) and Debian/Linux

**Engineering**
- CI/CD pipeline built with GitHub Actions to build and publish signed releases for both platforms
- License generation service tied to each machine's hardware fingerprint
