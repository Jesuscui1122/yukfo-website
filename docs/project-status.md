# YUKFO Website — Project Status

> 状态文件：防止未来 AI 会话无故"继续优化"。改网站前必须先读本文件。

## Current Status: Stable Release + Business Validation Phase

**不要再改网站**，除非出现以下触发条件之一。

## Completed (2026-08-27, baseline commit a896744)

- GEO entity correction (sourcing partner identity, four-site consistency)
- Multi-market static pages (us/uk/eu.yukfo.com, market-specific hero/FAQ/schema)
- Template + market-JSON build system (scripts/build.py)
- sitemap.xml + robots.txt per market, hreflang en matrix
- Homepage conversion: Hero dual CTA + 24h reply, How It Works 3-step flow
- Lead capture: form-only contact, FormSubmit activated & verified
- Worker routing: yukfo-router (market prefixes) + shiny-limit-af6b (static assets)

## Do Not Change Unless

- Customer feedback (real questions, objections, requests)
- Search Console / analytics data shows a specific problem
- Business requirement from Jesus

## Deliberately NOT Done (waiting for real material)

- Work page case enhancement (no fabricated numbers/cases/stories)
- /insights/ articles (no SEO content farm; content should come from real customer questions)
- Further Hero tweaking (marginal returns low)

## Next Triggers

- First customer questions → collect real language, use as future copy
- First completed projects → one real project > 10 SEO articles
- Search Console data (30-60 days) → only then evaluate

## Open Items (non-blocking)

- Search Console: add yukfo.com domain property → submit 4 sitemaps
- BR No.: add back after certificate verification (candidate 80477500)
- git push when network allows

Architecture details: see memory/geo-architecture-state.md
Entity definition: docs/geo-entity-definition.md
