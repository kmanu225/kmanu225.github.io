# 📚 Personal Academic Website

This repository hosts my **personal blog and academic portfolio**, built using the [**Academic Pages**](https://academicpages.github.io/) template — a modern, customizable Jekyll theme for GitHub Pages.

> Academic Pages is designed for researchers, students, and professionals to showcase their publications, projects, and achievements.

---

## 🚀 Getting Started

To set up your own site using this template:

1. **Sign up or log in** to [GitHub](https://github.com/) and verify your email.
2. Go to the [Academic Pages GitHub repo](https://github.com/academicpages/academicpages.github.io).
3. Click **“Use this template”** (top-right) to create your own copy.
4. Name the repo:
   ➤ `your-username.github.io`
   This will become your website’s URL:
   ➤ `https://your-username.github.io`
5. Customize your site content and `_config.yml` settings.
6. Add files (e.g., PDFs) to the `files/` directory. Access them at:
   ➤ `https://your-username.github.io/files/example.pdf`
7. To check publishing status, go to **Settings → Pages** in your repo.
8. *(Optional)* Use the Python/Jupyter tools in the `markdown_generator/` folder to generate publication pages from TSV files.

More setup help: [https://academicpages.github.io](https://academicpages.github.io/)

---

## 🧪 Running Locally

To preview your site locally before pushing:

### ✅ Requirements

Install dependencies:

* `ruby-dev`, `bundler`, `nodejs` (Linux/WSL)
* `ruby`, `node`, `bundler` (Mac)

**On WSL or Ubuntu:**

```bash
sudo apt update && sudo apt install ruby-dev ruby-bundler nodejs build-essential make
```

**On macOS (with Homebrew):**

```bash
brew install ruby node
gem install bundler
```

### ✅ Build and Serve

```bash
bundle install
bundle exec jekyll serve -l -H localhost
```

If you encounter permission errors:

```bash
bundle config set --local path 'vendor/bundle'
bundle install
```

---

## 🐳 Running with Docker

To avoid installing Ruby and Node locally, use the included `Dockerfile`:

```bash
docker compose up
```

Then open:
👉 `http://localhost:4000`

---

## 🔧 Maintenance & Contributions

* **Bug reports**: [Open an issue](https://github.com/academicpages/academicpages.github.io/issues/new/choose)
* **Theme help/discussion**: [Start a GitHub discussion](https://github.com/academicpages/academicpages.github.io/discussions)
* Based on [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/), licensed under MIT.

For submitting improvements:
➤ Fork the repo (instead of using the template)
➤ Sync your fork regularly to receive updates

---

## 🛡️ License and Credits

Maintained by [Robert Zupko](https://github.com/rjzupkoii), originally forked by [Stuart Geiger](https://github.com/staeiou).
Based on the MIT-licensed [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) theme.

---

<div align="center">

![pages-build-deployment](https://github.com/academicpages/academicpages.github.io/actions/workflows/pages/pages-build-deployment/badge.svg)
[![GitHub contributors](https://img.shields.io/github/contributors/academicpages/academicpages.github.io.svg)](https://github.com/academicpages/academicpages.github.io/graphs/contributors)
[![GitHub release](https://img.shields.io/github/v/release/academicpages/academicpages.github.io)](https://github.com/academicpages/academicpages.github.io/releases/latest)
[![GitHub license](https://img.shields.io/github/license/academicpages/academicpages.github.io?color=blue)](https://github.com/academicpages/academicpages.github.io/blob/master/LICENSE)

[![GitHub stars](https://img.shields.io/github/stars/academicpages/academicpages.github.io)](https://github.com/academicpages/academicpages.github.io)
[![GitHub forks](https://img.shields.io/github/forks/academicpages/academicpages.github.io)](https://github.com/academicpages/academicpages.github.io/fork)

</div>