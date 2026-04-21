#!/usr/bin/env node
// scripts/generate-search-index.js
// 运行方式: node scripts/generate-search-index.js
// Jekyll 构建后会调用此脚本更新搜索索引

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const POSTS_DIR = path.join(__dirname, '..', '_posts');

function getExcerpt(content) {
  // 去掉 frontmatter，取第一段作为摘要
  const lines = content.split('\n');
  let inFrontmatter = false;
  let excerptLines = [];
  let started = false;

  for (const line of lines) {
    if (line.trim() === '---') {
      if (!inFrontmatter) {
        inFrontmatter = true;
        continue;
      } else {
        inFrontmatter = false;
        started = true;
        continue;
      }
    }
    if (started && line.trim()) {
      // 去掉 Markdown 标题标记
      const clean = line.replace(/^#+\s*/, '').replace(/\*\*/g, '').replace(/\*/g, '').replace(/`/g, '').replace(/\{%.*?%\}/g, '').replace(/\{\{.*?\}\}/g, '');
      excerptLines.push(clean);
      if (excerptLines.length >= 2) break;
    }
  }

  return excerptLines.join(' ').substring(0, 200);
}

function slugify(filename) {
  return filename.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace(/\.md$/, '');
}

const files = fs.readdirSync(POSTS_DIR)
  .filter(f => f.endsWith('.md'))
  .sort()
  .reverse(); // 最新的在前面

const posts = [];

for (const file of files) {
  const filePath = path.join(POSTS_DIR, file);
  const raw = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(raw);

  const slug = slugify(file);
  const dateStr = typeof data.date === 'string' ? data.date : (data.date ? new Date(data.date).toISOString().split('T')[0] : '');
  const d = typeof data.date === 'string' ? new Date(data.date) : data.date;
  const url = `/posts/${d.getFullYear()}/${String(d.getMonth() + 1).padStart('2', '0')}/${String(d.getDate()).padStart('2', '0')}/${slug}/`;
  const excerpt = data.excerpt || getExcerpt(content);

  posts.push({
    title: data.title || slug,
    url,
    date: dateStr,
    categories: Array.isArray(data.categories) ? data.categories.join(',') : (data.categories || ''),
    tags: data.tags || [],
    excerpt: excerpt
  });
}

const searchPagePath = path.join(__dirname, '..', 'search', 'index.md');
const searchPage = fs.readFileSync(searchPagePath, 'utf8');

// 生成新的 searchData 块
const dataBlock = 'var searchData = ' + JSON.stringify(posts, null, 2) + ';';

// 替换旧的数据块
const newSearchPage = searchPage.replace(/var searchData = \[[\s\S]*?^\];/m, dataBlock + ';');

fs.writeFileSync(searchPagePath, newSearchPage, 'utf8');
console.log(`✅ 搜索索引已更新，共 ${posts.length} 篇文章`);
