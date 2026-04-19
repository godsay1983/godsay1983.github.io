#!/usr/bin/env python3
"""
scripts/generate-search-index.py
自动从 _posts/ 生成搜索索引，替换 search/index.md 中的 searchData
"""
import re
import os
from datetime import datetime
from pathlib import Path

POSTS_DIR = Path(__file__).parent.parent / '_posts'
SEARCH_PAGE = Path(__file__).parent.parent / 'search' / 'index.md'

def parse_frontmatter(content):
    """解析 Jekyll frontmatter"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, content
    fm_text = match.group(1)
    body = content[match.end():]
    fm = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.startswith('['):
                # 列表如 [tag1, tag2]
                val = val.strip('[]').split(',')
                val = [v.strip().strip('"').strip("'") for v in val if v.strip()]
            fm[key] = val
    return fm, body

def get_excerpt(body):
    """取正文第一段作为摘要"""
    lines = body.split('\n')
    excerpt_lines = []
    started = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        # 清理 Markdown 格式
        clean = re.sub(r'[#*`\[\]]', '', line).strip()
        if clean:
            excerpt_lines.append(clean)
            if len(excerpt_lines) >= 2:
                break
    return ' '.join(excerpt_lines)[:200]

def slug_from_filename(filename):
    """从文件名提取 slug"""
    return re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename).replace('.md', '')

def parse_date_from_filename(filename):
    """从文件名提取日期"""
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', filename)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return datetime.now()

posts = []
for f in sorted(POSTS_DIR.glob('*.md'), reverse=True):
    content = f.read_text(encoding='utf-8')
    fm, body = parse_frontmatter(content)
    slug = slug_from_filename(f.name)
    date = fm.get('date') or parse_date_from_filename(f.name)
    if isinstance(date, str):
        # 处理 "2026-04-19 12:30:00 +0800" 格式，只保留日期部分
        date_str = re.sub(r'\s+\d{2}:\d{2}:\d{2}\s*[+-]?\d{0,4}$', '', date).strip()
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except:
            date = parse_date_from_filename(f.name)

    url = f"/posts/{date.year}/{date.month:02d}/{date.day:02d}/{slug}/"
    excerpt = fm.get('excerpt') or get_excerpt(body)

    posts.append({
        'title': fm.get('title', slug),
        'url': url,
        'date': date.strftime('%Y-%m-%d'),
        'categories': fm.get('categories', ''),
        'tags': fm.get('tags', []),
        'excerpt': excerpt
    })

# 生成 searchData JS
js_lines = ['var searchData = [']
for p in posts:
    tags = p['tags'] if isinstance(p['tags'], list) else []
    excerpt = p['excerpt'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').strip()
    js_lines.append(f'  {{"title":"{p["title"]}","url":"{p["url"]}","date":"{p["date"]}","categories":"{p["categories"]}","tags":{tags},"excerpt":" {excerpt}"}},')
js_lines.append('];')

search_data_block = '\n'.join(js_lines)

# 读取 search/index.md，替换 searchData 块
search_page = SEARCH_PAGE.read_text(encoding='utf-8')
new_page = re.sub(r'var searchData = \[[\s\S]*?^\];', search_data_block + ';', search_page, flags=re.MULTILINE)

SEARCH_PAGE.write_text(new_page, encoding='utf-8')
print(f'✅ 搜索索引已更新，共 {len(posts)} 篇文章')
