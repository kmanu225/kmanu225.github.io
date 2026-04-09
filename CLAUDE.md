# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal academic website built with the [Academic Pages](https://academicpages.github.io/) Jekyll theme. It's a static site hosted on GitHub Pages showcasing publications, talks, teaching, portfolio, and blog posts.

## Build Commands

**Local Development:**
```bash
bundle install
bundle exec jekyll serve -l -H localhost
```
Server runs at `http://localhost:4000` (livereload on port 35729)

**With Docker:**
```bash
docker compose up
```
Sets `JEKYLL_ENV=docker` and mounts the current directory for live reloading.

**JavaScript Bundling:**
```bash
npm install
npm run build:js    # Minify JS assets
npm run watch:js    # Watch for JS changes
```

## Content Structure

This is a standard Jekyll site with these collections (defined in `_config.yml`):

- `_posts/` - Blog posts (filename format: `YYYY-MM-DD-title.md`)
- `_publications/` - Academic papers (front matter: `collection: publications`, `venue`, `citation`, `paperurl`, `slidesurl`)
- `_talks/` - Presentations/talks (front matter: `collection: talks`)
- `_teaching/` - Teaching experience (front matter: `collection: teaching`)
- `_portfolio/` - Project portfolio (front matter: `collection: portfolio`)
- `_pages/` - Static pages (e.g., `about.md` with `permalink: /`)

All collections output to `/_site/[collection-name]/`

## Content Generation Tools

The `markdown_generator/` directory contains Python scripts and Jupyter notebooks to bulk-generate content from TSV files:

- `publications.tsv` → `_publications/` (run `publications.py` or `publications.ipynb`)
- `talks.tsv` → `_talks/` (run `talks.py` or `talks.ipynb`)
- `PubsFromBib.ipynb` - Generate publications from BibTeX

**Required TSV columns for publications:** `pub_date` (YYYY-MM-DD), `title`, `venue`, `excerpt`, `citation`, `site_url`, `paper_url`, `url_slug`

These tools escape special characters for YAML and generate properly formatted markdown files with front matter. Run scripts from within the `markdown_generator/` directory.

## Key Configuration

- `_config.yml` - Main Jekyll config (site settings, author profile, collections, plugins)
- `Gemfile` - Ruby dependencies (includes `github-pages` gem for GitHub Pages compatibility)
- `package.json` - Node dependencies for JS minification
- `_data/cv.json` - JSON Resume format for CV page data

## Front Matter Patterns

**Blog posts:**
```yaml
---
title: 'Post Title'
date: 2025-03-15
tags:
  - tag-name
---
```

**Publications:**
```yaml
---
title: "Paper Title"
collection: publications
category: manuscripts  # or books, conferences
permalink: /publication/filename
date: 2025-01-01
venue: 'Journal Name'
excerpt: 'Brief summary or abstract'  # Optional
citation: 'Author. (2025). &quot;Title.&quot; <i>Journal</i>.'
paperurl: 'http://...'   # Optional
slidesurl: 'http://...'   # Optional
---
```

**Pages (like About):**
```yaml
---
permalink: /
title: "About Me"
author_profile: true
redirect_from:
  - /about/
---
```

## Layouts

- `single` - Standard content page (posts, publications, teaching)
- `talk` - Talk/presentation pages (includes talk map visualization if `talkmap_link: true` in `_config.yml`)
- `archive` - List pages (tags, categories)
- `cv-layout` - CV/resume page
- `default` - Base layout

## Assets

- Images: Place in `images/` directory
- PDFs: Place in `files/` directory
- Sass: Edit in `_sass/`, compiled to `_site/assets/css/`
- JavaScript: Source in `assets/js/`, bundled to `assets/js/main.min.js`

## Theme System

The site features two custom hacker themes:

1. **Hacker Theme** (`_sass/theme/_hacker.scss`): Matrix-style green-on-black with digital clock fonts
   - Uses Orbitron and Share Tech Mono fonts for a cyberpunk aesthetic
   - Features glowing link effects and terminal-style UI elements
   - Applied by default through JavaScript in `assets/js/_main.js`

2. **Hacker Light Theme** (`_sass/theme/_hacker-light.scss`): White background with dark text
   - Maintains the same digital fonts and green accents
   - Provides better readability for daylight viewing
   - Can be activated by changing the `site_theme` in `_config.yml`

Theme selection is controlled in `_config.yml` with the `site_theme` setting.

## JavaScript Architecture

Client-side functionality is implemented with:

- **jQuery** - DOM manipulation and event handling
- **FitVids** - Responsive video embedding
- **Magnific Popup** - Image lightbox galleries
- **jQuery Smooth Scroll** - Animated page scrolling

The build process bundles these dependencies:
1. Source files in `assets/js/` and `node_modules/` 
2. Processed by UglifyJS via `npm run build:js`
3. Output to `assets/js/main.min.js`

Custom JavaScript functionality includes:
- Theme initialization (always sets hacker theme)
- Sticky footer implementation
- Responsive navigation menus
- Image lightbox galleries
- Smooth scrolling navigation

## Important Notes

- The `_config.yml` file is **not** hot-reloaded; restart Jekyll after changes
- The site uses the **hacker theme** by default (Matrix-style green-on-black with digital clock fonts)
- **hacker-light theme** available: White background with dark text, same digital fonts and green accents
- `redirect_to` and `redirect_from` are available via jekyll-redirect-from plugin
- GitHub Pages auto-builds from `master` branch; no manual deployment needed
- The `webrick` gem is included for Ruby 3+ compatibility