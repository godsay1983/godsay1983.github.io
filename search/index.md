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
  {"title":"Hello, World! 我的第一篇博客","url":"/posts/2026/04/14/hello-world/","date":"2026-04-14","categories":"","tags":[],"excerpt":" 第一篇博客"},
  {"title":"跌宕起伏！三球准绝杀救赎，黄蜂加时险胜热火","url":"/posts/2026/04/15/nba-playin-hornets-heat/","date":"2026-04-15","categories":"","tags":[],"excerpt":" 比赛回顾"},
  {"title":"阿夫迪亚41+12创纪录！开拓者射落太阳，时隔5年重返季后赛","url":"/posts/2026/04/15/nba-playin-suns-blazers/","date":"2026-04-15","categories":"","tags":[],"excerpt":" 比赛回顾"},
  {"title":"OpenClaw vs Hermes：两大 AI Agent 平台深度对比","url":"/posts/2026/04/15/openclaw-vs-hermes/","date":"2026-04-15","categories":"","tags":[],"excerpt":" 前言"},
  {"title":"为什么有些人「等不了」任何结果？—— 不确定性焦虑解析","url":"/posts/2026/04/16/intolerance-of-uncertainty/","date":"2026-04-16","categories":"","tags":[],"excerpt":" 为什么有些人「等不了」任何结果？"},
  {"title":"马克西31分独自carry，76人击退魔术锁定季后赛席位","url":"/posts/2026/04/16/nba-playin-76ers-magic/","date":"2026-04-16","categories":"","tags":[],"excerpt":" 比赛回顾"},
  {"title":"末节三分雨逆转！库里35分率勇士击沉快船","url":"/posts/2026/04/16/nba-playin-warriors-clippers/","date":"2026-04-16","categories":"","tags":[],"excerpt":" 比赛回顾"},
  {"title":"使用 GitHub Pages 和内网 GitLab + Nginx 部署博客","url":"/posts/2026/04/16/双平台博客部署指南/","date":"2026-04-16","categories":"","tags":[],"excerpt":" 使用 GitHub Pages 和内网 GitLab + Nginx 部署博客"},
  {"title":"小米手机跌出前五：2026年Q1市场分析","url":"/posts/2026/04/17/xiaomi-q1-2026-analysis/","date":"2026-04-17","categories":"","tags":[],"excerpt":" 小米手机跌出前五：2026年Q1中国市场深度分析"},
  {"title":"小米股价跌至腰斩：2026年Q1股票深度分析","url":"/posts/2026/04/17/xiaomi-stock-analysis-q1-2026/","date":"2026-04-17","categories":"","tags":[],"excerpt":" 小米股价跌至腰斩：2026年Q1股票深度分析"},
  {"title":"AI时代的一人公司：一个人，凭什么撬动一家公司？","url":"/posts/2026/04/18/ai-shi-dai-yi-ren-gong-si/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 引言：当\"一个人创业\"不再是笑话"},
  {"title":"Claude 编程太贵了？2026年主流编程辅助方案全面对比","url":"/posts/2026/04/18/alternatives-to-claude-for-programming/","date":"2026-04-18","categories":"","tags":[],"excerpt":" Claude 编程太贵了？2026年主流编程辅助方案全面对比"},
  {"title":"Hermes 教程八：config.yaml深度配置","url":"/posts/2026/04/18/hermes-jiao-cheng-ba/","date":"2026-04-18","categories":"","tags":[],"excerpt":" Hermes Agent 进阶配置完全指南：模型、人格、工具开关"},
  {"title":"Hermes 教程二：零基础入门","url":"/posts/2026/04/18/hermes-jiao-cheng-er/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 零基础入门：5分钟跑通 Hermes Agent"},
  {"title":"Hermes 教程九：记忆系统","url":"/posts/2026/04/18/hermes-jiao-cheng-jiu/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 记忆系统：让 Hermes Agent 记住你的偏好"},
  {"title":"Hermes 教程六：编写自己的 Skill","url":"/posts/2026/04/18/hermes-jiao-cheng-liu/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 编写自己的 Skill：把重复操作自动化"},
  {"title":"Hermes 教程七：20+必备Skills推荐","url":"/posts/2026/04/18/hermes-jiao-cheng-qi/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 社区 Skills 大全：20+ 必备技能推荐"},
  {"title":"Hermes 教程三：思维链与追问技巧","url":"/posts/2026/04/18/hermes-jiao-cheng-san/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 让 AI 想清楚再回答：Hermes 的思维链与追问技巧"},
  {"title":"Hermes 教程十二：GitHub项目管理","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-er/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 用 Hermes Agent 管理 GitHub 项目：Issues 与 PR 实战"},
  {"title":"Hermes 教程十六：常见问题与解决方案","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-liu/","date":"2026-04-18","categories":"","tags":[],"excerpt":"使用 Hermes Agent 的过程中，可能会遇到一些常见问题。本文汇总了高频问题及其解决方案，帮助你快速排查和修复。"},
  {"title":"Hermes 教程十七：性能优化与Token节省","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-qi/","date":"2026-04-18","categories":"","tags":[],"excerpt":"在使用 Hermes Agent 时，性能优化是一个重要话题。本文介绍如何通过各种技术手段加快响应速度、节省 Token 消耗，让 Hermes 更加高效。"},
  {"title":"Hermes 教程十三：博客运营实战","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-san/","date":"2026-04-18","categories":"","tags":[],"excerpt":"用 Hermes 运营个人博客是一件非常高效的事情。本文详细介绍如何用 Hermes 实现博客文章从创作到发布的完整流程，以及如何配置双平台自动推送。"},
  {"title":"Hermes 教程十四：编程辅助方案对比","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-si/","date":"2026-04-18","categories":"","tags":[],"excerpt":"随着 AI 编程工具的快速发展，开发者有了更多选择。本文从功能、价格、使用体验等维度对比主流 AI 编程辅助工具，并探讨如何在 Hermes Agent 中集成这些工具。"},
  {"title":"Hermes 教程十五：MMX网络研究","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-wu/","date":"2026-04-18","categories":"","tags":[],"excerpt":"Hermes Agent 提供了强大的网络搜索和研究能力，特别是 MMX 搜索功能，可以帮助用户高效地收集和整理网络信息。本文详细介绍如何用 Hermes 进行网络研究，以及如何实现多源信息聚合。"},
  {"title":"Hermes 教程十一：MCP协议扩展","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-yi/","date":"2026-04-18","categories":"","tags":[],"excerpt":" MCP 协议：接入 100+ 外部工具的秘诀"},
  {"title":"Hermes 教程十：定时任务自动执行","url":"/posts/2026/04/18/hermes-jiao-cheng-shi/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 定时任务：让 Hermes Agent 每天自动执行"},
  {"title":"Hermes 教程四：飞书+QQ多平台配置","url":"/posts/2026/04/18/hermes-jiao-cheng-si/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 飞书 + QQ 同时在线：Hermes 多平台配置详解"},
  {"title":"Hermes 教程五：Skill 系统详解","url":"/posts/2026/04/18/hermes-jiao-cheng-wu/","date":"2026-04-18","categories":"","tags":[],"excerpt":" Skill 系统详解：Hermes 如何自动调用工具"},
  {"title":"Hermes 教程一：全面解析","url":"/posts/2026/04/18/hermes-jiao-cheng-yi/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 前言"},
  {"title":"附加赛单节崩盘！魔术31分大胜黄蜂，班凯罗25+5+6率队晋级","url":"/posts/2026/04/18/nba-playin-magic-vs-hornets/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 一、比赛概述"},
  {"title":"库里孤掌难鸣！太阳111-96力克勇士，杰伦·格林36分主导惊天爆冷","url":"/posts/2026/04/18/nba-playin-suns-vs-warriors/","date":"2026-04-18","categories":"","tags":[],"excerpt":" 一、比赛概述"}
];

var fuse = new Fuse(searchData, {
  keys: ['title', 'categories', 'tags', 'excerpt'],
  threshold: 0.3,
  includeMatches: true,
  minMatchCharLength: 1
});

function renderResults(results) {
  var html = '';
  if (results.length === 0) {
    html = '<div class="no-results">没有找到相关文章 😅</div>';
  } else {
    results.forEach(function(r) {
      var d = r.item;
      html += '<div class="search-result">';
      html += '<div><a href="' + d.url + '">' + d.title + '</a> <span class="date">' + d.date + '</span></div>';
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
