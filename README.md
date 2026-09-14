# kmanu225.github.io

Personal website of **Emmanuel Konan** - portfolio and blog, built with [Jekyll](https://jekyllrb.com/) on top of the [Academic Pages](https://academicpages.github.io/) theme, hosted on GitHub Pages.

The site features two custom "hacker" themes (Matrix-style green-on-black and a light variant), configurable via `site_theme` in `_config.yml`.

## Content

- `_posts/` - blog posts
- `_portfolio/` - project portfolio entries
- `_publications/`, `_talks/`, `_teaching/` - academic collections (currently unused, kept for future content)
- `_pages/` - static pages (e.g. `about.md`)
- `_data/cv.json` - CV/resume data (JSON Resume format)
- `images/`, `files/` - static assets and downloadable files (PDFs, etc.)

## Running locally

### Option A - Ruby/Jekyll directly

Requirements: Ruby (3.x), Bundler, Node.js.

Some gems (e.g. `bigdecimal`) build native extensions and need Ruby's development headers and a compiler. On Debian/Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y ruby3.2-dev build-essential
```

(Use the `-dev` package matching your installed Ruby version, e.g. `ruby3.2-dev`; check with `ruby -v`.)

**Windows:**

Install Ruby (with the MSYS2/DevKit toolchain needed to build native gem extensions) via [RubyInstaller](https://rubyinstaller.org/downloads/) - pick the "WITH DEVKIT" version. During setup, when prompted, run the `ridk install` step and select the MSYS2 base installation option.

Then, in a terminal (PowerShell or Command Prompt):

```powershell
gem install bundler
bundle install
bundle exec jekyll serve -l -H localhost
```

If `bundle install` fails with `make failed` / `No such file or directory - make` while building a native extension (e.g. `RedCloth`, `fast-stemmer`, `posix-spawn`, `yajl-ruby`, `redcarpet`, `racc`), the MSYS2/MinGW toolchain isn't installed. Fix it by running:

```powershell
ridk install
```

and choosing option **3** (MSYS2 and MINGW development toolchain) when prompted. Then re-run `bundle install`. If `ridk` isn't recognized at all, you installed the plain Ruby package instead of "WITH DEVKIT" - reinstall from [RubyInstaller](https://rubyinstaller.org/downloads/) using the DEVKIT variant.

The site is served at `http://localhost:4000` with livereload on port `35729`. `-l` enables livereload so the browser refreshes automatically on file changes.

If you hit permission errors installing gems:

```bash
bundle config set --local path 'vendor/bundle'
bundle install
```

> `_config.yml` is **not** hot-reloaded - restart `jekyll serve` after editing it.

### Option B - Docker

No local Ruby/Node install needed:

```bash
docker compose up
```

This builds the image from `Dockerfile`, mounts the repo for live editing, and serves at `http://localhost:4000` (livereload on `35729`).

### JavaScript changes

If you edit files under `assets/js/`, rebuild the minified bundle:

```bash
npm install
npm run build:js    # one-off build to assets/js/main.min.js
npm run watch:js    # rebuild automatically on change
```

## Generating content in bulk

The `markdown_generator/` directory has Python/Jupyter tools to turn TSV or BibTeX files into `_publications/` or `_talks/` markdown files. Run them from within that directory - see the scripts/notebooks for the expected columns.

## Deployment

The site auto-builds and deploys from the `master` branch via GitHub Pages - no manual deployment step needed. Push to `master` and check **Settings → Pages** in the repo for build status.

## Credits

Built on [Academic Pages](https://academicpages.github.io/), itself based on the [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) Jekyll theme (MIT licensed).
