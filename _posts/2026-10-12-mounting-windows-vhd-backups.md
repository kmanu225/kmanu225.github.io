---
title: "Mounting Windows VHD backups"
description: "Reading the contents of a .vhd backup image without restoring it."
date: 2026-10-12
lang: en
topic: software-engineering
guide_url: https://kmanu225.gitbook.io/cs/software-engineering/compatibility/mounting-windows-vhd-backups
tags:
  - software-engineering
  - windows
---

A `.vhd` backup image turned up during an engagement, and its contents were worth a look. A VHD is a virtual hard disk: a single file that holds a full disk image, including its partition table and file systems.

Instead of restoring the backup, you can attach the image as a block device and browse its file systems read-only. That keeps the original file untouched while giving access to the data it contains. The guide walks through mounting a VHD and inspecting its file systems.
