---
layout: post
title: "Hermes 教程六：编写自己的 Skill"
date: 2026-04-18 18:00:00 +0800
categories: [实战教程]
tags: [自定义Skill, 自动化, SKILL.md, 编写教程]
---

# 编写自己的 Skill：把重复操作自动化

Hermes 的 Skill 系统不仅仅用来安装社区技能，更重要的是你可以**自己编写 Skill**，把日常重复的工作流封装成可复用的自动化脚本。本文从零讲解如何编写一个真正可用的自定义 Skill。

## Skill 的最小结构

一个 Skill 最少只需要一个文件：

```
~/.hermes/skills/
└── my-daily-report/
    └── SKILL.md
```

`SKILL.md` 就是 Skill 的全部。试试这个最小的例子：

```markdown
---
name: my-daily-report
description: 生成每日工作汇报
---

# 每日汇报 Skill

你是一个专业的项目经理，擅长生成结构化的每日工作汇报。

当用户说"写日报"或"生成日报"时，执行以下步骤：

1. 首先询问：今天主要完成了哪些工作？（用户回复后继续）
2. 其次询问：遇到哪些问题？（可选，用户可跳过）
3. 最后询问：明天计划做什么？（用户回复后继续）

然后按以下格式整理输出：

## 📅 今日工作（{日期}）

### ✅ 完成事项
- ...

### ⚠️ 遇到的问题
- ...

### 🔄 明日计划
- ...

请使用 Markdown 格式，保持简洁专业。
```

把这个文件放到 `~/.hermes/skills/my-daily-report/SKILL.md`，然后：

```
hermes > /my-daily-report
```

Hermes 会自动加载这个 Skill，并按你的指令执行。

## Skill frontmatter 完整字段

```markdown
---
name: skill-name              # 必需，技能标识（英文、连字符）
description: 简短描述          # 必需，最大 1024 字符
version: 1.0.0                # 可选，语义版本
license: MIT                  # 可选，许可证
platforms: [linux, darwin]    # 可选，限制操作系统
                               #   有效值：linux, darwin, windows
                               #   省略则全平台可用
prerequisites:                 # 可选，运行要求（仅供参考）
  env_vars: [API_KEY]          #   需要的环保变量
  commands: [curl, jq]         #   需要的命令（仅提醒，不强制）
compatibility: Requires X       # 可选，兼容性说明
metadata:                      # 可选，扩展元数据
  hermes:
    tags: [tag1, tag2]         #   标签，用于搜索
    related_skills: [other]    #   相关技能
---

# Skill 正文
...
```

## 实战案例：封装 Git Code Review Skill

### 创建目录结构

```
~/.hermes/skills/code-review/
├── SKILL.md
└── references/
    └── review-checklist.md
```

### SKILL.md

```markdown
---
name: code-review
description: 自动化代码审查流程，检查风格、漏洞、性能问题
version: 1.0.0
platforms: [linux, darwin]
prerequisites:
  commands: [git, ruff, hadolint]
  env_vars: [GITHUB_TOKEN]
metadata:
  hermes:
    tags: [git, code-review, quality, devops]
---

# Code Review Skill

你是一个严格的代码审查员，帮助团队发现代码中的问题。

## 审查流程

当用户提供一个 Git diff 或仓库路径时，执行以下审查：

### 1. 代码风格检查

使用 `ruff check`（Python）或 `hadolint`（Dockerfile）：
\`\`\`bash
ruff check {file_path}
\`\`\`

### 2. 安全漏洞扫描

检查常见安全问题：
- 硬编码凭证
- SQL 注入风险
- XSS 漏洞模式
- 不安全的依赖版本

### 3. 性能检查

- N+1 查询问题
- 循环中的阻塞 IO
- 内存泄漏风险

### 4. 审查报告格式

统一输出：

```
## 🔍 Code Review Report

### 📁 文件
{file_path}

### ✅ 通过项
- ...

### ⚠️ 警告项
- ...

### ❌ 问题项（需修复）
- [严重] {描述} → {修复建议}
- [中等] {描述} → {修复建议}
- [轻微] {描述} → {修复建议}

### 📊 总结
- 严重问题：N
- 中等问题：N
- 轻微问题：N
```

### 参考资料

完整检查清单见 `references/review-checklist.md`。
```

### references/review-checklist.md

```markdown
# Code Review Checklist

## Python
- [ ] 使用 `ruff` 检查代码风格
- [ ] 无硬编码密码或密钥
- [ ] 使用参数化查询（防 SQL 注入）
- [ ] 关闭数据库/文件句柄
- [ ] 异步代码无阻塞调用

## General
- [ ] 函数长度不超过 50 行
- [ ] 无重复代码（DRY 原则）
- [ ] 适当的错误处理
- [ ] 文档字符串完整
```

## 调用 Skill 的方式

### 方式一：斜杠命令（最常用）

```
hermes > /code-review
```

### 方式二：在对话中自然触发

```
hermes > 帮我 review 一下刚才改的那个文件
# 如果文件名与某个 Skill 名称匹配，会自动加载
```

### 方式三：嵌套在其他 Skill 中

在一个 Skill 的正文中调用另一个 Skill：

```markdown
## 其他任务

如果用户需要处理 Git 相关任务，请调用 `/git-helper` 技能。
```

## Skill 之间的数据传递

Skill 之间通过对话上下文共享数据。例如：

```
用户：帮我写一个 PPT
Hermes（加载 /pptx skill）
→ 用户：我已经有一份数据报告了
→ Hermes（加载 /data-extract skill，从报告中提取数据）
→ Hermes（将提取的数据注入 /pptx skill，生成 PPT）
```

## 工具调用在 Skill 中的使用

Skill 描述中引用工具时，AI 模型会自动决定调用哪些 Tool：

```markdown
## 工作流程

1. 使用 `ReadFile` 工具读取项目配置文件
2. 分析项目结构
3. 使用 `RunCommand` 执行代码格式化
4. 将结果写入报告
```

`ReadFile`、`RunCommand` 等工具名会被模型识别并自动调用对应的 Tool handler。

## 为 Skill 添加配置变量

Skill 可以声明配置变量，在使用时动态填充：

```markdown
---
name: deploy-helper
description: 一键部署应用到服务器
metadata:
  hermes:
    config_vars:
      - key: server_host
        description: 服务器地址
        required: true
      - key: deploy_path
        description: 部署路径
        default: /var/www/app
---

# Deploy Helper

将代码部署到 {server_host} 的 {deploy_path} 目录。
```

配置变量通过 `~/.hermes/config.yaml` 的 `skills.config.*` 路径存储：

```yaml
skills:
  config:
    deploy_helper:
      server_host: "39.108.142.88"
      deploy_path: "/var/www/app"
```

## Skill 的调试技巧

### 查看所有已注册的 Skill 命令

```bash
hermes > /help
# 找到 Skill Commands 部分
```

### 检查 Skill 是否被正确识别

```python
# 在 Python 中验证
from agent.skill_utils import get_all_skills_dirs, skill_matches_platform
from pathlib import Path

skills_dirs = get_all_skills_dirs()
for d in skills_dirs:
    print(d)
```

### 查看 Skill 加载的详细日志

启动 Hermes 时加上 `--verbose`：

```bash
hermes --verbose
```

## 分发你的 Skill

如果你想把自己写的 Skill 分享给团队或社区：

1. 将 Skill 目录打包（或提交到 Git）
2. 其他人放到 `~/.hermes/skills/` 即可使用
3. 也可以提交到 Hermes Skills Hub（通过 `/skills publish` 命令）

## 小结：Skill 编写检查清单

- [ ] `SKILL.md` 放在 `~/.hermes/skills/<skill-name>/` 下
- [ ] `name` 字段英文小写，用连字符分隔
- [ ] `description` 清晰描述 Skill 用途
- [ ] frontmatter 填写 platforms、prerequisites 等
- [ ] 正文用 Markdown，工具调用用自然语言描述
- [ ] 参考文档放在 `references/` 子目录
- [ ] 建议先用简单对话测试，再逐步完善

Skill 是 Hermes 自动化能力的核心——你编写的每个 Skill，都是在给 AI 添加一个专业技能，让它能帮你处理越来越复杂的工作流。
