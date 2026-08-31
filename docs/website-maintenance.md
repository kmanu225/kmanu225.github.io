# Maintaining the portfolio

The public site is English-only. Its primary positioning is applied cryptography, PKI/HSM and IT/OT/IoT security. It remains a static, GitHub Pages-compatible Jekyll site; no framework migration or production deployment is required to preview these changes.

## Content sources

- `_includes/home.html`: homepage narrative and selected work.
- `_data/cv.json`: shared source for the HTML CV and downloadable PDF.
- `_portfolio/`: case studies, ordered by `rank`. Set `portfolio_categories` to one or more IDs from `_data/portfolio_categories.yml`. A project appears in each assigned category; its content and URL remain unique. The OT/IoT audit overview belongs to both security audits and industrial systems.
- `_data/portfolio_categories.yml`: the four portfolio headings, their order, anchor IDs and icons. The full homepage expertise cards link to these sections using native links with visible keyboard focus.
- `_posts/`: English article summaries. `guide_url` links to the original external guide without automatically redirecting the reader. Keep existing `redirect_from` aliases.
- `_data/navigation.yml`: primary navigation.
- `assets/css/professional.css`: the active stylesheet, independent of the legacy theme styles.
- `_includes/icon.html`: local SVG icons used by navigation, links and expertise cards. Keep icons decorative (`aria-hidden`) and retain visible link labels. Navigation icon names are set in `_data/navigation.yml`.
- `assets/js/professional.js`: progressive-enhancement navigation; no tracking or browser storage.

The homepage uses a full portrait beside the introduction on desktop. At 780px and below, it sits beside the action buttons and social links. Preserve the image's natural proportions; do not restore a fixed-height crop. The four expertise cards include cryptography and PQC even when adapting the visual layout.

## Build and preview

Use Ruby/Bundler for Jekyll, Node.js 22+ for development tools, and Python 3 with `reportlab` and `pypdf` for the CV. The CV renderer also needs Arial (Windows) or DejaVu Sans (Linux). `pypdfium2` is optional for PDF screenshots.

```sh
bundle install
npm install
npx playwright install chromium
python3 -m pip install reportlab pypdf pypdfium2
python3 scripts/build_cv.py --render
npm run build:assets
bundle exec jekyll build
npm run test:site -- _site
bundle exec jekyll serve --host 127.0.0.1
```

On Windows, use `python` instead of `python3` if appropriate. In this repository's WSL setup, run Jekyll inside Ubuntu. A built output directory may also be passed to the browser tests from Windows using its UNC path.

The checked-in PDF and image derivatives allow ordinary Jekyll builds without Python, Sharp or Playwright. Rebuild the PDF after editing CV data; rebuild image assets after changing the source portrait or sharing-card design.

Generated PDF review copies go under `output/pdf`; the published copy goes under `files`. Test reports and screenshots go under `tmp`. Both intermediate directories, maintenance docs and scripts are excluded from the public site.

## Verification coverage

The browser regression script serves only the generated directory on a loopback address and checks:

- Every HTML page listed in the sitemap: title, description, canonical, English language, structured data, one main heading and named links/images.
- All local links, image/script/stylesheet references and fragment targets found on those pages.
- Automated axe checks for WCAG A/AA rules, plus mobile homepage checks.
- Representative pages at 320, 390, 768, 1024 and 1440 pixels, checking horizontal overflow.
- Keyboard skip link, mobile menu open/close, Escape focus return and navigation with JavaScript disabled.
- Legacy bookmark responses, PDF availability and absence of unnecessary external rendering dependencies.

Screenshots still need human review. Automated accessibility checks do not establish full WCAG conformance. Local tests do not establish production Core Web Vitals or search-engine indexing. Check the deployed site and Search Console separately when available.

## Writing style

Use plain, factual English. Describe what was done, the tools used and the scope of the work. Avoid slogans, self-assessments and generic conclusions repeated across articles. The homepage should introduce the author and point to the work without restating the CV. Avoid featuring the same guide as both a project and an article on the homepage.

Keep specific limitations where readers need them: draft status, coauthorship, lab scope and confidentiality. Do not add a disclaimer about a result the text never suggests. Article summaries should introduce the subject briefly; the shared GitBook link provides access to the full guide.

## Editorial checks before applying

- Confirm certificate issuing bodies and credential links before adding them; none have been invented.
- Confirm the exact personal contribution to joint work before expanding the EAP-PSK-256 case study.
- Only add measured results or client-specific examples when documented and authorized for public disclosure.
- Keep the distinction between an individual Internet-Draft and an approved standard. Check the IETF record when updating its status.
- The OT/IoT page is a non-confidential methodology overview, not a fabricated client case study.
- The PKI page is a learning lab, not evidence of production HSM deployment.
- External GitBook content remains separately maintained; the FICOBA source is in French, while the site summary is English.
- Ask a recruiter and a technical consultant to review the site before a major public launch.

## Publication

Building or previewing does not publish the site. Review the diff, including any changes that predated this redesign, before committing and pushing through the repository's normal GitHub Pages workflow. Never overwrite unrelated work to roll back a layout change.
