---
layout: home
title: 欢迎来到我的博客
---

## 欢迎 👋

这是一个用 Jekyll 和 GitHub Pages 创建的个人博客。

在这里我会分享：
- 📝 技术笔记
- 💡 思考和想法
- 🌟 其他有趣的内容

## 最新文章

{% for post in site.posts limit:5 %}
- {{ post.date | date: "%Y-%m-%d" }} [{{ post.title }}]({{ post.url }})
{% endfor %}
