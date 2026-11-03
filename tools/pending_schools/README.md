# Schools imported without a Google rating (2026-11-03)

The 97 schools in `candidates-2026-11-03.json` were added to the country data files (fr, es, it, pt, ee) with
rating `None, None`. They appear in the rankings and city pages after the rated schools, without points or a place,
labelled "Final score not yet available". Each entry has the URL that was fetched and an evidence quote.

To add real ratings: fill `ratings-to-fill.csv` (rating and review count from Google Maps), then replace
`None, None` for that school in `tools/<country>_data.py` with the rating and review count, rebuild
(`build_<cc>.py`, `build_<cc>_schools.py`, `build_hub.py`, `link_schools.py`, `clean_urls.py`, `build_en.py`) and run the audit.
Weak entries to double check: directory-only URLs, general dance schools whose Bachata mention came from a regional list.
