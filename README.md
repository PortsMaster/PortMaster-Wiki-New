# PortMaster Wiki

The PortMaster website: game browser, port pages, install guides, porter docs,
porter tools and news. It's a static site built with
[MkDocs](https://www.mkdocs.org/) and the
[Material](https://squidfunk.github.io/mkdocs-material/) theme, with a Python
build script that pulls in the live port data. It's hosted on Cloudflare
Workers.

## Running it locally

### What you need

- **Git**, to clone the repo.
- **Python 3** with **pip**. On Debian/Ubuntu: `sudo apt install python3 python3-pip python3-venv`.
  On Windows/macOS, use the installer from [python.org](https://www.python.org/downloads/).

### Install the Python packages

Do this once, from the repo folder. A virtual environment keeps the packages out of
your system Python. It's optional, but recent Linux distributions refuse a plain
system-wide `pip install`.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install mkdocs-material mkdocs-glightbox mkdocs-macros-plugin pillow
```

| Package | What it's for |
|---|---|
| `mkdocs-material` | MkDocs itself plus the Material theme |
| `mkdocs-macros-plugin` | runs `main.py` and fills in the `{{ ... }}` template tags in pages |
| `mkdocs-glightbox` | click-to-zoom for images |
| `pillow` | image checks for the homepage mosaic. Optional: the build works without it. |

These are the same packages Cloudflare installs for its builds (see `wrangler.jsonc`).
If you used a virtual environment, run `source .venv/bin/activate` again in each new
terminal before building.

### Build and serve

```bash
FAST_BUILD=1 mkdocs build
python3 -m http.server 8642 --directory site
```

Then open <http://localhost:8642>. Rebuild after each change, then reload the
browser.

- **`FAST_BUILD=1`** skips downloading the port data from GitHub and reuses
  the copies already in `docs/assets/json/`. A build takes a few seconds this
  way.
- **Leave `FAST_BUILD` off** for a full build with fresh data. That's what
  Cloudflare runs. It's slower and needs internet access.
- **Avoid `mkdocs serve`.** The build writes generated JSON files into `docs/`,
  which `mkdocs serve` sees as changes, so it can end up rebuilding in a loop.

## Making changes

### Edit a page

Pages are Markdown files in `docs/`. The URL follows the path:
`docs/installation/runtimes.md` becomes `/installation/runtimes/`. Edit the
file, rebuild, and check it in the browser.

Besides normal Markdown you can use:

- admonitions (`!!! tip "Title"`)
- tables
- `{ .md-button }` buttons
- Mermaid diagrams

The full list of Markdown extensions is under `markdown_extensions` in
`mkdocs.yml`.

### Add a page

1. Create the Markdown file somewhere under `docs/`, for example
   `docs/contribute/porting/engines/unity.md`.
2. Add it to `nav:` in `mkdocs.yml` where it should appear in the menu:
   ```yaml
   - Engines:
       - Godot: contribute/porting/engines/godot.md
       - Unity: contribute/porting/engines/unity.md
   ```
   A page that isn't in `nav:` still gets built, but you can only reach it by
   its URL.
3. Rebuild and check it.

### Write a news post

1. Add a Markdown file to `docs/news/posts/`, using an existing post such as
   `november-2026-potm.md` as a template.
2. The front matter needs a `date`, `authors` and `readtime`.
3. Each author must be listed in `docs/news/.authors.yml`.
4. Put `<!-- more -->` where the preview on the news page should stop. Every
   post needs it.

The newest posts also show up on the homepage automatically.

### Change the Games page banner

The big banner on the Games page shows games picked from the images in
`docs/assets/images/hero/`:

- **Add a game:** drop in `<port_id>.jpg`, `.png` or `.webp`, e.g. `balatro.jpg`.
- **Remove a game:** delete its image.
- **More than five images:** five are picked at random on every build.

The curated rows below the banner ("PortMaster Picks" and so on) come from
`docs/assets/json/featured_ports.json`.

### Change styling

The CSS lives in `docs/assets/stylesheets/`, one file per area (`homepage.css`,
`port-page.css`, `porter-tools.css`, …). They're all listed under `extra_css`
in `mkdocs.yml`. Theme colours and global tweaks are in `extra.css`.

## Repository layout

```
docs/                     Site content - everything here ends up on the site
  index.md                Homepage (hero, live stats, get involved, latest news)
  games.md                Games page: Discover (hero, carousels) + Browse (filters, Steam check)
  port.md                 Single port page (/port/?name=<id>), filled in by javascripts/port-page.js
  porter.md, porters.md   Porter profile page and porter list
  installation/           Player guides (install PortMaster, ports, runtimes, handhelds)
  contribute/             Porter and contributor docs (porting, engines, GUI, packaging)
  tools/                  Porter tools: JSON / README / gameinfo generators, cover maker, ...
  news/                   Blog: index.md, posts/, .authors.yml
  faq.md, community/      FAQ and community pages
  javascripts/            Page scripts (port-page.js, tablesort.js)
  assets/
    stylesheets/          All custom CSS
    images/               Logos, hero images (hero/), homepage images (home/)
    json/                 Port data (see below)
overrides/                Theme template overrides (the header Donate button)
main.py                   Build script (mkdocs-macros): downloads data, builds page variables
mkdocs.yml                Site config: theme, nav menu, plugins, CSS list
wrangler.jsonc            Cloudflare Worker config for the website
worker/scheduled.js       Cron that triggers rebuilds (every 12h + after new port releases)
workers/steam-api/        Separate Worker behind the Steam library check
site/                     Build output (not committed)
```

The pages with real app logic are `games.md`, `port.md`, `porter.md`,
`porters.md`, `index.md` and everything in `tools/`. They're mostly HTML and
JavaScript inside Markdown files, using Jinja template tags
(`{{ ... }}`, `{% ... %}`) that `main.py` fills in at build time. The rest of
the site is plain Markdown documentation.

## Where the data comes from

`main.py` runs at the start of every build. On a full build it downloads the
port data into `docs/assets/json/`:

| File | Source |
|---|---|
| `ports.json`, `runtimes_zips.json` | latest release of [PortMaster-New](https://github.com/PortsMaster/PortMaster-New) |
| `ports-MV.json` | latest release of PortMaster-MV-New |
| `port_stats.json`, `porters.json`, `device_info.json` | [PortMaster-Info](https://github.com/PortsMaster/PortMaster-Info) |

From those it generates the files the pages load in the browser:

- `port_details.json`: everything the port page, games page and tools need
- `porter_details.json`: porter pages
- `runtime_archs.json`: the device compatibility checks

It also sets the template variables used in the pages: port counts, stats,
hero slides, the latest news and so on.

These files are edited by hand and never downloaded:

- `featured_ports.json`: the curated game rows
- `suggestions_new.json`: the Port Suggestions page
- `screenshot_bars.json`: a cache the homepage mosaic uses

To fix data such as a port's description or a device's firmware list, change
it in PortMaster-New or PortMaster-Info. It shows up here on the next build.

## Deployment

Hosting is on Cloudflare, in the team account:

- **Website:** the `portmaster-wiki` Worker, built from this repo's root.
- **Steam API:** the `steam-api` Worker, built from `workers/steam-api/`.

A site update starts when any of these happens:

- **A push to `main`:** both Workers rebuild.
- **A new PortMaster-New or PortMaster-MV-New release:** picked up within
  about 15 minutes.
- **Every 12 hours** (00:00 and 12:00 UTC), as a safety net.

The schedule is in `worker/scheduled.js`. It starts builds through a deploy
hook stored as the `DEPLOY_HOOK_URL` secret on the Worker.

The secrets for the scheduled rebuilds and the Steam API key are stored in
Cloudflare, not in this repo.
