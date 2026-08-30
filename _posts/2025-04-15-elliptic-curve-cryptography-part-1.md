---
title: "Elliptic-curve cryptography: the mathematical foundation"
description: "An introduction to elliptic curves and the distinction between mathematical structure and secure protocol implementation."
date: 2025-04-15
modified: 2026-08-31
lang: en
topic: cryptography
guide_url: https://kmanu225.gitbook.io/cs/cryptography/elliptic-curve-cryptography/part-1-what-are-elliptic-curves
tags:
  - cryptography
redirect_from:
  - /blog-post-2/
---

## Why start with the mathematics?

Elliptic-curve cryptography builds protocols on mathematical structures with efficient operations and computationally difficult inverse problems. Understanding that foundation helps explain how relatively compact keys can support public-key operations.

Comparisons with RSA require equivalent security levels; equal key lengths do not imply equal security.

## What this introduction covers

This is the first part of my series on elliptic curves. It introduces the objects and geometric intuition before the second part moves to finite fields.

## From theory to engineering

The mathematics is only a starting point. A deployed system also needs appropriate parameters, validated inputs and carefully implemented operations.

For applied work, I would separate the choice of cryptographic scheme from implementation assurance and key lifecycle management. An introductory derivation should not become a production cryptographic library.
