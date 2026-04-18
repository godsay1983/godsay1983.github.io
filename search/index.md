---
layout: default
title: 文章搜索
permalink: /search/
---
<style>
.search-container { margin: 2rem 0; }
.search-input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  font-size: 1rem;
}
.search-input:focus { outline: none; border-color: var(--accent); }
#search-results { margin-top: 1.5rem; }
.search-result {
  padding: 1rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  margin-bottom: 0.8rem;
  background: var(--bg-secondary);
}
.search-result a { font-size: 1.1rem; font-weight: bold; color: var(--accent); }
.search-result .date { color: var(--text-muted); font-size: 0.9rem; margin-left: 0.5rem; }
.search-result .excerpt { color: var(--text-muted); margin-top: 0.3rem; font-size: 0.95rem; }
.no-results { color: var(--text-muted); padding: 2rem; text-align: center; }
mark { background: #4a3f00; color: #ffd700; padding: 0 2px; border-radius: 2px; }
</style>

<h2>🔍 文章搜索</h2>
<div class="search-container">
  <input type="text" id="search-input" class="search-input" placeholder="输入关键词搜索标题、分类或标签..." autofocus>
</div>
<div id="search-results" class="no-results">输入关键词开始搜索...</div>

<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js"></script>
<script>
// 文章数据（由 scripts/generate-search-index.js 生成，Jekyll 构建时自动更新）
var searchData = [
  {"title":"Hello, World! 我的第一篇博客","url":"/posts/2026/04/14/hello-world/","date":"2026-04-14","categories":"随想","tags":[],"excerpt":"大家好，我是曹总。这是我用 Jekyll + GitHub Pages 创建的个人博客。"},
  {"title":"NBA 附加赛：Hornets vs Heat","url":"/posts/2026/04/15/nba-playin-hornets-heat/","date":"2026-04-15","categories":"NBA","tags":[],"excerpt":""},
  {"title":"NBA 附加赛：Suns vs Blazers","url":"/posts/2026/04/15/nba-playin-suns-blazers/","date":"2026-04-15","categories":"NBA","tags":[],"excerpt":""},
  {"title":"OpenClaw vs Hermes","url":"/posts/2026/04/15/openclaw-vs-hermes/","date":"2026-04-15","categories":"AI","tags":[],"excerpt":""},
  {"title":"双平台博客部署指南","url":"/posts/2026/04/16/双平台博客部署指南/","date":"2026-04-16","categories":"技术","tags":[],"excerpt":""},
  {"title":"不确定性容忍度","url":"/posts/2026/04/16/intolerance-of-uncertainty/","date":"2026-04-16","categories":"心理学","tags":[],"excerpt":""},
  {"title":"NBA 附加赛：76ers vs Magic","url":"/posts/2026/04/16/nba-playin-76ers-magic/","date":"2026-04-16","categories":"NBA","tags":[],"excerpt":""},
  {"title":"NBA 附加赛：Warriors vs Clippers","url":"/posts/2026/04/16/nba-playin-warriors-clippers/","date":"2026-04-16","categories":"NBA","tags":[],"excerpt":""},
  {"title":"小米 2026 Q1 分析","url":"/posts/2026/04/17/xiaomi-q1-2026-analysis/","date":"2026-04-17","categories":"商业","tags":[],"excerpt":""},
  {"title":"小米股票 2026 Q1 分析","url":"/posts/2026/04/17/xiaomi-stock-analysis-q1-2026/","date":"2026-04-17","categories":"投资","tags":[],"excerpt":""},
  {"title":"AI 时代一人公司","url":"/posts/2026/04/18/ai-shi-dai-yi-ren-gong-si/","date":"2026-04-18","categories":"AI","tags":[],"excerpt":""},
  {"title":"Claude 替代方案对比","url":"/posts/2026/04/18/alternatives-to-claude-for-programming/","date":"2026-04-18","categories":"AI","tags":[],"excerpt":""},
  {"title":"Hermes 教程八","url":"/posts/2026/04/18/hermes-jiao-cheng-ba/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程二","url":"/posts/2026/04/18/hermes-jiao-cheng-er/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程九","url":"/posts/2026/04/18/hermes-jiao-cheng-jiu/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程六","url":"/posts/2026/04/18/hermes-jiao-cheng-liu/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程七","url":"/posts/2026/04/18/hermes-jiao-cheng-qi/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程三","url":"/posts/2026/04/18/hermes-jiao-cheng-san/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程十","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-er/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程十六","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-liu/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程四","url":"/posts/2026/04/18/hermes-jiao-cheng-si/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程十二","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-yi/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程十三","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-san/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程十四","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-si/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程十五","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-wu/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程十一","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-yi/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程五：Skill 系统详解","url":"/posts/2026/04/18/hermes-jiao-cheng-wu/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""},
  {"title":"Hermes 教程一","url":"/posts/2026/04/18/hermes-jiao-cheng-yi/","date":"2026-04-18","categories":"核心机制","tags":[],"excerpt":""}
];

var fuse = new Fuse(searchData, {
  keys: ['title', 'categories', 'tags', 'excerpt'],
  threshold: 0.3,
  includeMatches: true,
  minMatchCharLength: 1
});

function highlight(text, indices) {
  if (!indices || !indices.length) return text;
  var result = '';
  var lastIndex = 0;
  indices.forEach(function(pair) {
    result += text.slice(lastIndex, pair[0]);
    result += '<mark>' + text.slice(pair[0], pair[1] + 1) + '</mark>';
    lastIndex = pair[1] + 1;
  });
  result += text.slice(lastIndex);
  return result;
}

function renderResults(results) {
  var html = '';
  if (results.length === 0) {
    html = '<div class="no-results">没有找到相关文章 😅</div>';
  } else {
    results.forEach(function(r) {
      var d = r.item;
      var titleHighlighted = highlight(d.title, r.matches && r.matches.find(function(m){ return m.key==='title'; }) ? r.matches.find(function(m){ return m.key==='title'; }).indices[0] : null);
      html += '<div class="search-result">';
      html += '<div><a href="' + d.url + '">' + titleHighlighted + '</a> <span class="date">' + d.date + '</span></div>';
      if (d.excerpt) html += '<div class="excerpt">' + d.excerpt.substring(0, 120) + (d.excerpt.length > 120 ? '...' : '') + '</div>';
      html += '</div>';
    });
  }
  document.getElementById('search-results').innerHTML = html;
}

function doSearch(query) {
  if (!query.trim()) {
    document.getElementById('search-results').innerHTML = '<div class="no-results">输入关键词开始搜索...</div>';
    return;
  }
  var results = fuse.search(query);
  renderResults(results);
}

document.addEventListener('DOMContentLoaded', function() {
  var params = new URLSearchParams(window.location.search);
  var q = params.get('q');
  if (q) {
    document.getElementById('search-input').value = q;
    doSearch(q);
  }
  document.getElementById('search-input').addEventListener('input', function(){ doSearch(this.value); });
  document.getElementById('search-input').addEventListener('keypress', function(e){
    if(e.key==='Enter'){ doSearch(this.value); }
  });
});
</script>
