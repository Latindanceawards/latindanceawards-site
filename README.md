# Latin Dance Awards

Website for latindanceawards.com: the independent Bachata awards (Germany 2026 edition).

- `index.html` homepage (German, with English switch)
- `bewerbung.html` free school application
- `rankings.html` rankings with countdown to December 20, 2026 (`?preview=1` shows sample data)
- `automation/emails.gs` Google Apps Script that sends the application emails
- `tools/build.py` regenerates `bewerbung.html` and `rankings.html` from the homepage's header, footer and styles

Hosted on Cloudflare Pages. Every push to `main` deploys automatically.

## Build notes (URLs)
Cloudflare Pages redirects `/x.html` to `/x` and `/dir/index.html` to `/dir/`. After running the build scripts, run `python3 tools/clean_urls.py` (idempotent) so canonical, hreflang, og:url, JSON-LD, sitemap.xml, llms.txt and internal links all use the extensionless URLs. `tools/seo_audit.py` checks this.
