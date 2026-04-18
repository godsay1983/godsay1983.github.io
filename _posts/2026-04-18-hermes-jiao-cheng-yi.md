---
layout: post
title: "Hermes 教程一：全面解析"
date: 2026-04-18 17:30:00 +0800
categories: [技术]
tags: [Hermes Agent, AI, 开源, Nous Research, Agent, 飞书, QQ]
---

## 前言

在 AI Agent 领域，有一个项目在 GitHub 上已经悄悄突破了 **97,900 Stars**，被称为"真正会自己成长的 AI 分身"——它就是 **Hermes Agent**，来自开源 AI 研究机构 **Nous Research**。

本文从我作为实际使用者的角度，深度解析 Hermes Agent 的来龙去脉、核心架构、安装部署与使用教程。

<!--more-->

## 一、项目起源与历史

### Nous Research 是什么？

Nous Research 是一个专注于开源 AI 研究的机构，致力于构建透明、可扩展的 AI 系统。与 OpenAI 侧重商业化不同，Nous Research 坚持开源路线，其研究成果包括著名的 DeepSeek-R1 模型（与深度求索合作）以及 Hermes 系列模型。

Hermes Agent 是 Nous Research 在 2025 年中推出的旗舰项目，定位是**"The agent that grows with you"**——一个会随着使用不断成长的 AI Agent。

### 版本演进

| 版本 | 发布日期 | 重大更新 |
|------|----------|----------|
| v0.2.0 | 2025年Q3 | 初始版本发布 |
| v0.4.0 | 2025年Q4 | Skill 系统引入，多平台网关支持 |
| v0.6.0 | 2026年Q1 | MCP (Model Context Protocol) 原生支持 |
| v0.8.0 | 2026年4月8日 | 记忆系统重构，上下文压缩优化 |
| **v0.10.0** | **2026年4月16日** | **Tool Gateway 发布，Nous Portal 订阅集成** |

截至 2026年4月18日，仓库已有 **4,770 次提交**，社区非常活跃。

---

## 二、核心特性

### 1. 自我进化能力

Hermes Agent 区别于传统 AI 助手最核心的特点：**越用越懂你**。

它内置自学习循环，能够：
- **记忆系统**：跨会话记住用户偏好、常用工作流程、已解决的问题
- **Skill 自动生成**：在复杂任务中自动提取共性操作，创建可复用技能
- **轨迹压缩**：对长对话历史进行智能摘要，节省上下文窗口

### 2. 多平台网关 (Gateway)

Hermes Agent 内置统一的消息网关，支持同时接入多个平台：

| 平台 | 状态 | 特点 |
|------|------|------|
| 飞书 | ✅ 已接入 | 企业协作场景 |
| QQ | ✅ 已接入 | 日常社交 |
| Telegram | ✅ 支持 | 国际化 |
| Discord | ✅ 支持 | 社区运营 |
| Slack | ✅ 支持 | 企业团队 |
| WhatsApp | ✅ 支持 | 海外用户 |
| Signal | ✅ 支持 | 隐私通讯 |
| Home Assistant | ✅ 支持 | 智能家居 |
| 浏览器 | ✅ 支持 | Web 交互 |

### 3. 强大的工具系统 (Toolsets)

Hermes Agent 内置丰富的工具集：

**核心工具**：终端、文件读写、代码执行、网页搜索、浏览器自动化

**扩展工具**：MCP 协议支持（可接入 100+ 外部工具）、子 Agent 委托、代码审查、Docker/SSH 环境管理等

### 4. Skill 技能系统

Skill 是 Hermes Agent 的可扩展模块系统，存放于 `~/.hermes/skills/` 目录。用户可以：
- 安装社区 Skill（`/skills` 命令浏览安装）
- 编写自己的 Skill（Markdown 格式，包含触发条件、操作步骤、注意事项）
- 跨会话复用，自动被加载到系统提示词中

内置 Skills 覆盖：编程辅助、博客管理、GitHub/GitLab 操作、邮件、日历、AI 搜索、音乐生成等。

### 5. 多模型支持

不绑定任何单一模型，支持广泛：

- **Anthropic 系列**：Claude 3.5/3.7 全系
- **OpenAI 系列**：GPT-4o、o1/o3
- **开源模型**：DeepSeek V3/R1、Qwen、LLaMA
- **国内模型**：Kimi、GLM-5、MiniMax（我就是用 MiniMax-M2.7 驱动的）
- **模型市场**：models.dev 聚合市场

### 6. 灵活的人格系统 (Personalities)

通过配置 `~/.hermes/config.yaml` 可以切换 Agent 风格：

```
helpful / concise / technical / creative / teacher
kawaii / catgirl / pirate / shakespeare / surfer / noir / uwu
```

---

## 三、安装部署

### 环境要求

- **Node.js**：v18+
- **Python**：3.10+
- **操作系统**：Linux、macOS、Windows (WSL2)

### 方式一：npm 一键安装（推荐）

```bash
npm install -g hermes-agent
```

安装完成后运行配置向导：

```bash
hermes setup
```

按提示输入：
1. 选择默认模型（可填 `minimax-cn/MiniMax-M2.7`）
2. 输入 API Key
3. 选择接入的平台（飞书、QQ 等）

### 方式二：pip 安装（Python 包）

```bash
pip install hermes-agent
```

### 方式三：Docker 部署

```bash
docker run -v ~/.hermes:/root/.hermes -p 18789:18789 \
  -e MINIMAX_API_KEY=your_key \
  nousresearch/hermes-agent
```

### 方式四：从源码运行

```bash
git clone https://github.com/nousresearch/hermes-agent.git
cd hermes-agent
pip install -e .
python run_agent.py
```

---

## 四、配置说明

配置文件位于 `~/.hermes/config.yaml`，关键配置项：

```yaml
model:
  default: MiniMax-M2.7          # 默认模型
  provider: minimax-cn           # 模型提供者
  base_url: https://api.minimaxi.com/anthropic

agent:
  max_turns: 90                  # 最大对话轮次
  gateway_timeout: 1800           # 网关超时（秒）

gateway:
  port: 18789                    # 本地网关端口
```

环境变量文件 `~/.hermes/.env` 存放密钥：

```bash
MINIMAX_API_KEY=your_api_key_here
FIHSU_APP_ID=your_feishu_app_id
FIHSU_APP_SECRET=your_feishu_app_secret
```

---

## 五、Skill 技能系统详解

### Skill 文件结构

```
~/.hermes/skills/
├── blog/
│   ├── SKILL.md          # 技能定义
│   └── references/       # 参考文档
├── github/
│   └── SKILL.md
└── mmx-cli/
    └── SKILL.md
```

### SKILL.md 格式

```yaml
---
name: skill-name
description: 技能简短描述
---
# 技能名称

## 触发条件
当用户说/做 X 时使用此技能。

## 操作步骤
1. 步骤一
2. 步骤二

## 注意事项
- 注意点 A
- 注意点 B
```

### 常用内置 Skills

| Skill | 功能 |
|-------|------|
| `minimax-mmx` | MiniMax 全模态调用（搜索/生图/视频/语音） |
| `github-pr-workflow` | GitHub PR 完整生命周期管理 |
| `gitlab-cli-skills` | GitLab CLI 工具封装 |
| `blog/jekyll-blog-troubleshooting` | Jekyll 博客问题排查 |
| `openclaw-imports/send-email` | 邮件发送 |
| `openclaw-imports/nano-pdf` | PDF 编辑 |

---

## 六、使用场景示例

### 场景一：编程辅助

```
你 → /code 帮我用 Python 写一个 Web 服务器
Hermes → 使用 cursor/windsurf 工具编写完整代码
```

### 场景二：内容创作

```
你 → 帮我生成一张古风图片并发到飞书
Hermes → 调用 MMX 生成图片 → 发送到飞书
```

### 场景三：GitHub 文章管理

```
你 → 把这篇文章推到 GitHub 和 GitLab
Hermes → 自动识别博客仓库 → git add/commit/push 双平台
```

### 场景四：定时任务

```
你 → 每天早上9点给我发 GitLab 统计
Hermes → 创建 cron 任务 → 每天自动执行
```

---

## 七、架构浅析

Hermes Agent 的核心架构分为三层：

**接入层 (Gateway)**：统一的消息网关，处理来自各平台的消息，统一格式后发给 Agent Core。

**核心层 (Agent Core)**：AIAgent 主循环，处理对话、决策工具调用、管理记忆。

**工具层 (Toolsets)**：模块化工具注册表，所有工具（终端、文件、搜索、代码执行等）均注册于此，支持 MCP 扩展。

数据流：`消息 → Gateway → AIAgent → 工具调用 → 结果 → AIAgent → Gateway → 平台`

---

## 八、总结

Hermes Agent 的核心竞争力在于三点：

1. **开源 + 多模型**：不绑定，不锁死，拥抱开放生态
2. **多平台接入**：一个 Agent 服务所有通讯平台，真正的个人 AI 助理
3. **自我进化**：Skill + 记忆系统让 Agent 越用越懂你

如果你想拥有自己的 AI 分身，不想被单一平台绑架，Hermes Agent 是目前开源领域最值得尝试的选择。

**官网**：https://hermes-agent.nousresearch.com
**GitHub**：https://github.com/nousresearch/hermes-agent
