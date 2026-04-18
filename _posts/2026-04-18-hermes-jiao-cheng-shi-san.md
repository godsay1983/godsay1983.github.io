---
layout: post
title: "Hermes 教程十三：博客运营实战"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [博客运营, Jekyll, GitHub, GitLab, 自动化]
---

用 Hermes 运营个人博客是一件非常高效的事情。本文详细介绍如何用 Hermes 实现博客文章从创作到发布的完整流程，以及如何配置双平台自动推送。

## Jekyll 博客管理

Hermes 内置了 `blog/jekyll-blog-troubleshooting` Skill，专门用于 Jekyll 博客的常见问题诊断和日常维护。常用的博客管理操作包括：

- `bundle exec jekyll serve` 本地预览博客
- `bundle exec jekyll build` 构建静态文件
- 排查 Liquid 模板错误、分类/标签问题
- 修复 permalink 格式问题

博客工作目录通常位于 `/home/xxxt-ubuntu/blog/`，文章存放在 `_posts/` 子目录中。

## 写文章的标准流程

用 Hermes 写博客文章的标准流程非常简洁：

1. **使用 write_file 工具创建文章文件**，文件命名格式为 `YYYY-MM-DD-文章标题.md`，存放在 `_posts/` 目录下
2. **编写文章内容**，遵循 Jekyll 的 front matter 格式（layout、title、date、categories、tags）
3. **本地预览**（可选）：在 blog 目录下运行 `bundle exec jekyll serve` 查看效果
4. **Git 提交**：`git add . && git commit -m "添加文章：标题"`
5. **推送到远程仓库**：`git push origin main`

整个流程都可以在 Hermes 对话中完成，无需切换到终端。

## 双平台推送

曹总的博客配置了 GitHub 和 GitLab 双平台同步：

- **GitHub**：托管在 `godsay1983.github.io`，面向公网读者
- **GitLab**：部署在 `192.168.109.202:4000`，用于内网访问和备份

双平台推送配置步骤：

```bash
# 添加两个 remote
git remote add github https://github.com/godsay1983/godsay1983.github.io.git
git remote add gitlab http://192.168.109.202:8080/xxxt-ubuntu/blog.git

# 推送到两个平台
git push github main
git push gitlab main
```

或者在 `.git/config` 中配置 `push.default = matching`，一次 push 同时推送到所有 remote。

## 自动化的 cron 推送方案

对于定期更新的博客，可以配置 cron 任务实现自动化推送。在 `/home/xxxt-ubuntu/.hermes/cron/` 目录下创建定时任务：

```python
# cron/publish_blog.py
import subprocess
import sys
sys.path.insert(0, '/home/xxxt-ubuntu/.hermes')
from hermes_state import SessionDB

def publish_pending_articles():
    """检查待发布的草稿并自动推送"""
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd='/home/xxxt-ubuntu/blog',
        capture_output=True, text=True
    )
    if result.stdout.strip():
        subprocess.run(['git', 'add', '.'], cwd='/home/xxxt-ubuntu/blog')
        subprocess.run(['git', 'commit', '-m', '自动发布更新'], cwd='/home/xxxt-ubuntu/blog')
        subprocess.run(['git', 'push', 'github', 'main'], cwd='/home/xxxt-ubuntu/blog')
        subprocess.run(['git', 'push', 'gitlab', 'main'], cwd='/home/xxxt-ubuntu/blog')
```

配置 crontab：`0 */6 * * * python3 /home/xxxt-ubuntu/.hermes/cron/publish_blog.py`，每 6 小时自动检查并推送更新。

## 曹总博客案例

曹总的博客是使用 Hermes 运营个人博客的典型案例：

- **公网地址**：https://godsay1983.github.io
- **内网地址**：http://192.168.109.202:4000
- **仓库结构**：使用 Jekyll 主题，配合 Hermes 的文章模板
- **更新频率**：每天更新多篇高质量文章

通过 Hermes 的 write_file + git commit + push 组合，每次创作完成后可以直接在对话中完成整个发布流程，真正实现"专注写作，无需操心技术"。

## 总结

用 Hermes 运营博客的核心优势：

| 环节 | 传统方式 | Hermes 方式 |
|------|---------|-------------|
| 写文章 | 打开编辑器 | 对话式创作 |
| 预览 | 手动启动服务 | 一句话完成 |
| 发布 | 多次命令操作 | 自动完成 |
| 双平台 | 手动推两个仓库 | 一次 push 全平台 |

Hermes 让博客运营变得简单高效，是内容创作者的理想助手。
