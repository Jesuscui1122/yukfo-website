#!/usr/bin/env python3
"""YUKFO GEO build verification (Step 3, zero deps).

Checks dist/ (or a custom out dir) for:
  A. title / meta description / canonical per market page
  B. hero H1 / sub / CTA on index
  C. market differentiation signals in title+meta
  D. JSON-LD schema: Organization + Service + FAQPage, @id domain,
     market-specific areaServed, FAQ count parity with page
  E. hreflang matrix (4-way, en not de-de)
  F. URL routing readiness: dist/ global at root, markets in us/ uk/ eu/
     with shared assets

Usage:
  python -X utf8 scripts/verify_geo.py            # check dist/
  python -X utf8 scripts/verify_geo.py --out dist
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index', 'services', 'work', 'contact', 'thanks']
SITEMAP_PAGES = ['/', '/services', '/work', '/contact']
MARKETS = ['global', 'us', 'uk', 'eu']
MARKET_SIGNAL = {
    'global': None,
    'us': ['US', 'United States'],
    'uk': ['UK', 'United Kingdom'],
    'eu': ['EU', 'Europe'],
}
AREA = {'global': 'Worldwide', 'us': 'United States',
        'uk': 'United Kingdom', 'eu': 'Europe'}
DOMAIN = {'global': 'yukfo.com',
          'us': 'us.yukfo.com', 'uk': 'uk.yukfo.com', 'eu': 'eu.yukfo.com'}

FAILS = []


def fail(mkt, page, msg):
    FAILS.append(f'[{mkt}/{page}] {msg}')


def get_html(out, mkt, page):
    path = os.path.join(out) if mkt == 'global' else os.path.join(out, mkt)
    p = os.path.join(path, page + '.html')
    if not os.path.exists(p):
        fail(mkt, page, 'file missing')
        return None
    with open(p, encoding='utf-8') as f:
        return f.read()


def title_of(s):
    m = re.search(r'<title>(.*?)</title>', s)
    return m.group(1).strip() if m else ''


def meta_desc(s):
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    return m.group(1) if m else ''


def hreflangs(s):
    return re.findall(r'hreflang="([^"]+)" href="([^"]+)"', s)


def schemas(s):
    return [json.loads(m) for m in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', s, re.S)]


def text_of(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(ROOT, 'dist'))
    args = ap.parse_args()
    out = args.out

    print('=' * 60)
    print('GEO BUILD VERIFICATION')
    print('=' * 60)

    # F. routing readiness: structure first
    print('\n[F] URL ROUTING READINESS')
    for mkt in MARKETS:
        d = out if mkt == 'global' else os.path.join(out, mkt)
        missing = [p for p in PAGES
                   if not os.path.exists(os.path.join(d, p + '.html'))]
        status = f'{len(PAGES) - len(missing)}/5 pages'
        if missing:
            fail(mkt, '-', f'missing: {missing}')
            status += ' MISSING!'
        print(f'  {mkt:7s} {d}  {status}')
    for extra in ('assets', '_redirects'):
        ok = os.path.exists(os.path.join(out, extra))
        print(f'  {"OK " if ok else "MISS"} shared/{extra}')
        if not ok:
            fail('-', '-', f'shared {extra} missing')

    # sitemap.xml + robots.txt per market (Step 3.5)
    print('\n[G] SITEMAP / ROBOTS')
    for mkt in MARKETS:
        d = out if mkt == 'global' else os.path.join(out, mkt)
        domain = DOMAIN[mkt]
        sm = os.path.join(d, 'sitemap.xml')
        if not os.path.exists(sm):
            fail(mkt, '-', 'sitemap.xml missing')
            continue
        content = open(sm, encoding='utf-8').read()
        locs = re.findall(r'<loc>(.*?)</loc>', content)
        expect = [f'https://{domain}{u}' for u in SITEMAP_PAGES]
        if locs != expect:
            fail(mkt, '-', f'sitemap locs {locs} != {expect}')
        if 'thanks' in content:
            fail(mkt, '-', 'sitemap contains thanks (noindex)')
        rb = os.path.join(d, 'robots.txt')
        if not os.path.exists(rb):
            fail(mkt, '-', 'robots.txt missing')
        elif f'Sitemap: https://{domain}/sitemap.xml' not in open(rb, encoding='utf-8').read():
            fail(mkt, '-', 'robots Sitemap line wrong')
        print(f'  {mkt:7s} sitemap {len(locs)} URLs + robots ✅')

    # per market per page
    for mkt in MARKETS:
        print(f'\n=== {mkt.upper()} ===')
        domain = DOMAIN[mkt]
        base = f'https://{domain}/'
        for page in PAGES:
            s = get_html(out, mkt, page)
            if s is None:
                continue
            # A. title / meta / canonical
            t = title_of(s)
            md = meta_desc(s)
            if not t:
                fail(mkt, page, 'empty <title>')
            print(f'  {page:9s} title: {t[:70]}')
            if page != 'thanks':
                m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
                if m and not m.group(1).startswith(base):
                    fail(mkt, page, f'canonical {m.group(1)} != {base}{"" if page=="index" else page}')
                hf = hreflangs(s)
                keys = {k for k, _ in hf}
                if keys != {'en-us', 'en-gb', 'en', 'x-default'}:
                    fail(mkt, page, f'hreflang keys {sorted(keys)}')
                if 'de-de' in keys:
                    fail(mkt, page, 'de-de still present')
                xdef = [v for k, v in hf if k == 'x-default']
                if xdef != ['https://yukfo.com/' + ('' if page == 'index' else page)]:
                    fail(mkt, page, f'x-default {xdef}')

            # B. hero on index
            if page == 'index':
                h1 = text_of(re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))
                sub = re.search(r'class="sub">(.*?)</p>', s)
                cta = re.search(r'class="btn" href="contact">(.*?)</a>', s)
                print(f'  H1: {h1}')
                if sub:
                    print(f'  SUB: {text_of(sub.group(1))}')
                if cta:
                    print(f'  CTA: {cta.group(1)}')
                if not h1 or not sub or not cta:
                    fail(mkt, 'index', 'hero incomplete')

            # C. market signal in title/meta (index/services only: those carry
            #    the market intent; work/contact/thanks stay brand-uniform)
            sig = MARKET_SIGNAL[mkt]
            if sig and page in ('index', 'services'):
                hay = (t + ' ' + md).lower()
                if not any(x.lower() in hay for x in sig):
                    fail(mkt, page, f'market signal {sig} missing in title/meta')

            # D. schema
            if page in ('index', 'contact'):
                ss = schemas(s)
                if not ss:
                    fail(mkt, page, 'no JSON-LD')
                    continue
                graph = ss[0].get('@graph', [])
                types = [n.get('@type') for n in graph]
                if 'Organization' not in types:
                    fail(mkt, page, 'Organization missing')
                if 'Service' not in types:
                    fail(mkt, page, 'Service missing')
                for n in graph:
                    if n.get('@type') == 'Organization':
                        if n.get('@id') != base + '#org':
                            fail(mkt, page, f'org @id {n.get("@id")}')
                    if n.get('@type') == 'Service':
                        if n.get('areaServed') != AREA[mkt]:
                            fail(mkt, page,
                                 f'areaServed {n.get("areaServed")} != {AREA[mkt]}')
                    if n.get('@type') == 'FAQPage':
                        nq = len(n.get('mainEntity', []))
                        pq = s.count('class="faq-item"')
                        if nq != pq:
                            fail(mkt, page, f'FAQPage {nq} vs page {pq}')
                        if page != 'contact':
                            fail(mkt, page, 'FAQPage on non-contact page')
                        print(f'  FAQPage: {nq} questions == page {pq} ✅')

    print('\n' + '=' * 60)
    if FAILS:
        print(f'FAIL: {len(FAILS)} issues')
        for f in FAILS:
            print('  ' + f)
        sys.exit(1)
    print('ALL CHECKS PASSED ✅')
    print('=' * 60)


if __name__ == '__main__':
    main()
