#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yukfo.com 文案铁律校验器（stdlib only）。
用法:
  python -X utf8 scripts/check_copy.py              # 全站检查（根目录 *.html）
  python -X utf8 scripts/check_copy.py --page work  # 单页检查
硬失败(退出码1): 违禁词 / 正文破折号 / href 双引号 / 必备事实缺失
警告(退出码0): 绝对化词(人工判断) / 词数带
"""
import re, sys, html, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARD_WORDS = ['trusted', 'my own production', 'own factory', "i've shipped", 'guarantee']
WARN_WORDS = [' always', 'everything', 'never']
MUST_KEEP = {
    'index':    ['No category limits'],
    'services': ['PA6', 'ABS', 'PP', 'EVA', 'IXPE'],
    'work':     ['26-SKU'],
    'contact':  ['24 hours', '30%', '70%'],
}
BASELINE_WORDS = {'index': 78, 'services': 558, 'work': 168, 'contact': 508}
PAGE_BAND = (0.70, 1.10)   # 上界放宽：v3.1 信任包（hero 数字条/实体锚点/表单隐藏字段）有意新增少量词
TOTAL_BAND = (0.70, 1.10)  # 上界放宽：8/25 改版 5→4 页，词数结构性下降后重校

def raw(page):
    return open(os.path.join(ROOT, page + '.html'), encoding='utf-8').read()

def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)

def page_words(page):
    return len(re.findall(r'[A-Za-z0-9]+', strip_tags(raw(page))))

def body_text(page):
    m = re.search(r'<body[^>]*>(.*)</body>', raw(page), flags=re.S)
    return strip_tags(m.group(1)) if m else ''

def check(page):
    errs, warns = [], []
    s = raw(page)
    # 1) 正文破折号（head 里的标题分隔符不算）
    b = body_text(page)
    for ch in ('—', '–'):
        if ch in b:
            errs.append(f'正文破折号 {ch!r} x{b.count(ch)}')
    # 2) 违禁词（全页含 head）
    low = s.lower()
    for w in HARD_WORDS:
        n = low.count(w)
        if n:
            lines = [str(i + 1) for i, l in enumerate(s.splitlines()) if w in l.lower()]
            errs.append(f'违禁词 {w!r} x{n} 行 {",".join(lines)}')
    for w in WARN_WORDS:
        n = low.count(w)
        if n:
            lines = [str(i + 1) for i, l in enumerate(s.splitlines()) if w in l.lower()]
            warns.append(f'绝对化词 {w.strip()!r} x{n} 行 {",".join(lines)}（人工判断）')
    # 3) href 双引号 bug
    n = len(re.findall(r'href="[^"]*""', s))
    if n:
        errs.append(f'href 双引号残留 x{n}')
    # 4) 必备事实
    for k in MUST_KEEP.get(page, []):
        if k not in s:
            errs.append(f'必备事实 {k!r} 缺失')
    # 5) 词数带
    w = page_words(page)
    base = BASELINE_WORDS.get(page)
    if base is None:
        print(f'  ok 词数 {w}（无基线，跳过带检查）')
    else:
        ratio = w / base
        if not (PAGE_BAND[0] <= ratio <= PAGE_BAND[1]):
            warns.append(f'词数 {w}（基线 {base}，{ratio:.0%}）超出带 {PAGE_BAND[0]:.0%}-{PAGE_BAND[1]:.0%}')
        else:
            print(f'  ok 词数 {w}（{ratio:.0%}）')
    return errs, warns

def main():
    args = sys.argv[1:]
    if args and args[0] == '--page':
        if len(args) < 2:
            print('usage: check_copy.py [--page <name>]', file=sys.stderr)
            sys.exit(2)
        pages = args[1:]
    else:
        pages = [os.path.splitext(os.path.basename(p))[0] for p in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
    bad, n_err, n_warn = False, 0, 0
    total_w = total_base = 0
    for p in pages:
        if not os.path.exists(os.path.join(ROOT, p + '.html')):
            print(f'{p}.html: FAIL')
            print(f'  ERR 页面不存在')
            bad = True
            n_err += 1
            continue
        errs, warns = check(p)
        print(f'{p}.html: {"PASS" if not errs else "FAIL"}')
        for e in errs:
            print(f'  ERR {e}')
        for w in warns:
            print(f'  WARN {w}')
        if errs:
            bad = True
        n_err += len(errs)
        n_warn += len(warns)
        w = page_words(p)
        base = BASELINE_WORDS.get(p)
        if base is not None:
            total_w += w
            total_base += base
    if len(pages) > 1:
        if total_base > 0:
            r = total_w / total_base
            flag = '' if TOTAL_BAND[0] <= r <= TOTAL_BAND[1] else '（超出全站带）'
            print(f'全站合计 {total_w} 词 / 基线 {total_base}（{r:.0%}）{flag}')
        else:
            print(f'全站合计 {total_w} 词（无基线页面）')
    print(f'\n{"FAIL" if bad else "PASS"}: {n_err} 错误, {n_warn} 警告')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
