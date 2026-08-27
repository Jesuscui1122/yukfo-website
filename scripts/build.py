#!/usr/bin/env python3
"""YUKFO multi-market static site generator. Zero dependencies.

Usage:
  python -X utf8 scripts/build.py                 # build all markets
  python -X utf8 scripts/build.py --market global # build one market only

Templates in src/templates/*.html.template contain {{placeholders}}.
Market data in src/markets/<market>.json supplies values per page.
Output goes to dist/ (global at root, markets in us/ uk/ eu/).
"""
import argparse
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_DIR = os.path.join(ROOT, 'src', 'templates')
MKTS_DIR = os.path.join(ROOT, 'src', 'markets')
OUT = os.path.join(ROOT, 'dist')
ASSETS = os.path.join(ROOT, 'assets')

PAGES = ['index', 'services', 'work', 'contact', 'thanks']
MARKET_FILES = ['global.json', 'us.json', 'uk.json', 'eu.json']
SHARED = ['_redirects']
SITEMAP_PAGES = ['/', '/services', '/work', '/contact']  # thanks is noindex
DOMAIN = {'global': 'yukfo.com',
          'us': 'us.yukfo.com', 'uk': 'uk.yukfo.com', 'eu': 'eu.yukfo.com'}

INDENT_HREFLANG = ''
INDENT_FAQ = '      '
INDENT_SCHEMA = ''

SCHEMA_PAGES = ('index', 'contact')


def make_schema(base_url, area, faqs):
    """Auto-generate JSON-LD: Organization + Service (areaServed) + FAQPage.

    Data lives in market JSON; HTML is generated here, so the JSON stays
    HTML-free. areaServed is market-specific (Worldwide / United States /
    United Kingdom / Europe).
    """
    org = {
        '@type': 'Organization',
        '@id': base_url + '#org',
        'name': 'YUKFO',
        'url': base_url,
        'address': {'@type': 'PostalAddress', 'addressCountry': 'HK'},
    }
    svc = {
        '@type': 'Service',
        'name': 'China sourcing services',
        'serviceType': 'Sourcing',
        'areaServed': area,
        'provider': {'@id': base_url + '#org'},
    }
    graph = [org, svc]
    if faqs:
        graph.append({
            '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': f['q'],
                 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}}
                for f in faqs
            ],
        })
    payload = json.dumps({'@context': 'https://schema.org', '@graph': graph},
                         ensure_ascii=False, indent=2)
    return '<script type="application/ld+json">\n' + payload + '\n</script>'


def build_blocks(data):
    """Build derived HTML blocks (hreflang / faq additions / schema) per page.

    Values are joined without leading indent: the first line sits on the
    template placeholder line (which carries its own indentation), following
    lines get the indent prefix. Empty values are left empty so the caller
    can drop the placeholder line entirely.
    """
    blocks = {}
    for page, p in data['pages'].items():
        hf = p.get('hreflang', {})
        hf_lines = [
            f'<link rel="alternate" hreflang="{k}" href="{v}" />'
            for k, v in hf.items()
        ]
        blocks[(page, 'hreflang_block')] = (
            ('\n' + INDENT_HREFLANG).join(hf_lines) if hf_lines else '')

        faqs = p.get('faq', [])
        faq_lines = [
            f'<details class="faq-item"><summary>{f["q"]}</summary>'
            f'<p>{f["a"]}</p></details>'
            for f in faqs
        ]
        blocks[(page, 'faq_list')] = (
            ('\n' + INDENT_FAQ).join(faq_lines) if faq_lines else '')
    return blocks


def render_page(page, data, blocks):
    path = os.path.join(TPL_DIR, f'{page}.html.template')
    with open(path, 'r', encoding='utf-8', newline='') as f:
        t = f.read()
    crlf = '\r\n' in t  # template line ending governs output
    p = data['pages'][page]

    # 0. schema: auto-generated JSON-LD on index/contact
    if page in SCHEMA_PAGES:
        domain = ('yukfo.com' if data['market'] == 'global'
                  else f"{data['market']}.yukfo.com")
        faqs = p.get('faq', []) if page == 'contact' else []
        t = t.replace('{{schema_block}}',
                      make_schema(f'https://{domain}/',
                                  data.get('area_served', 'Worldwide'), faqs))

    # 1. derived blocks: only replace non-empty (empty stays as placeholder,
    #    dropped as a whole line in step 3 to keep byte-exact output)
    for (pg, key), val in blocks.items():
        if pg == page and val:
            t = t.replace('{{' + key + '}}', val)

    # 2. scalar fields
    for k, v in p.items():
        if k in ('hreflang', 'faq'):
            continue
        t = t.replace('{{' + k + '}}', str(v))

    # 3. drop lines that still hold an empty placeholder (whole line removed)
    t = re.sub(r'^[ \t]*\{\{\w+\}\}[ \t]*\r?\n', '', t, flags=re.M)

    # 4. normalize line endings to the template's own (blocks join with \n)
    if crlf:
        t = t.replace('\r\n', '\n').replace('\n', '\r\n')

    # 4. warn on any placeholder the data did not provide
    leftovers = sorted(set(re.findall(r'\{\{(\w+)\}\}', t)))
    if leftovers:
        print(f'  WARN {page}: missing fields -> {leftovers}')
    return t


def main():
    ap = argparse.ArgumentParser(description='Build YUKFO market sites')
    ap.add_argument('--market', choices=['global', 'us', 'uk', 'eu'], default=None)
    args = ap.parse_args()

    files = [f for f in MARKET_FILES
             if args.market is None or f.startswith(args.market + '.')]

    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    for fn in files:
        with open(os.path.join(MKTS_DIR, fn), encoding='utf-8') as f:
            data = json.load(f)
        mkt = data['market']
        target = OUT if mkt == 'global' else os.path.join(OUT, mkt)
        os.makedirs(target, exist_ok=True)
        blocks = build_blocks(data)
        for page in PAGES:
            html = render_page(page, data, blocks)
            with open(os.path.join(target, f'{page}.html'), 'w',
                      encoding='utf-8', newline='') as f:
                f.write(html)
        print(f'{mkt}: {len(PAGES)} pages')

    # shared assets / config at global root
    shutil.copytree(ASSETS, os.path.join(OUT, 'assets'))
    for s in SHARED:
        src = os.path.join(ROOT, s)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(OUT, s))
    # NOTE: routing lives in the Worker script (Workers Static Assets mode),
    # edited in Cloudflare Dashboard — not deployable via the static uploader.
    # per-market sitemap.xml + robots.txt (generated, market-specific)
    for fn in files:
        mkt = json.load(open(os.path.join(MKTS_DIR, fn), encoding='utf-8'))['market']
        domain = DOMAIN[mkt]
        target = OUT if mkt == 'global' else os.path.join(OUT, mkt)
        locs = '\n'.join(
            f'  <url><loc>https://{domain}{u}</loc>'
            f'<priority>{"1.0" if u == "/" else "0.9"}</priority></url>'
            for u in SITEMAP_PAGES)
        sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                   + locs + '\n</urlset>\n')
        with open(os.path.join(target, 'sitemap.xml'), 'w',
                  encoding='utf-8', newline='\n') as f:
            f.write(sitemap)
        robots = ('User-agent: *\nAllow: /\n\n'
                  f'Sitemap: https://{domain}/sitemap.xml\n')
        with open(os.path.join(target, 'robots.txt'), 'w',
                  encoding='utf-8', newline='\n') as f:
            f.write(robots)
    print(f'done -> {OUT}')


if __name__ == '__main__':
    main()
