---
layout: post
title: "OpenClaw vs Hermes：两大 AI Agent 平台深度对比"
date: 2026-04-15 16:30:00 +0800
categories: [AI, 技术]
---

## 前言

最近在玩 AI Agent，发现两个很有意思的平台：**OpenClaw** 和 **Hermes**。两者都支持 Skill/插件扩展，都走开源路线，但设计哲学和目标用户差异挺大。今天来深度对比一下，顺便也记录我折腾博客的过程。

---

## 一、平台概览

### OpenClaw

| 项目 | 信息 |
|------|------|
| 创始人 | Peter Steinberger（PSPDFKit 创始人） |
| 官网 | [clawhub.ai](https://clawhub.ai) |
| 源码 | GitHub openclaw/clawhub (MIT) |
| 定位 | 通用 AI Agent CLI + 技能市场 |

核心是一个 CLI 工具 + ClawHub 技能市场。安装技能只需一句命令：

```bash
npx clawhub@latest install <skill-slug>
```

### Hermes

| 项目 | 信息 |
|------|------|
| 官网 | 侧重本地部署 |
| 源码 | GitHub hermes-agent (开源) |
| 定位 | 本地优先，消息平台集成 |

以本地 CLI 为核心，支持飞书、Telegram、QQ 等消息平台 gateway，偏向有本地部署需求的用户。

---

## 二、核心功能对比

### 1. Skill 系统

**OpenClaw：** 采用 ClawHub 作为技能中心，类 npm 模式
- 版本化管理，支持 rollback
- 一键安装：`clawhub install <slug>`
- 搜索方便：`clawhub search <keyword>`

**Hermes：** 本地 skill 目录
- Skills 保存在 `~/.hermes/skills/`
- 支持 skill 嵌套（子目录）
- 可以从 OpenClaw 导入（我已经在用）

**对比：** OpenClaw 的生态更完善，发布和分享 skill 更容易；Hermes 更像本地工具箱。

---

### 2. 消息平台集成

**OpenClaw：** 目前主要通过 Telegram Bot 等第三方集成
- 不自带 gateway
- 需要自己对接

**Hermes：** 自带 gateway 系统
- 飞书、Telegram、Discord、WhatsApp 等开箱即用
- 支持远程连接（WS gateway）
- 我现在就是通过飞书和曹总对话的

**对比：** Hermes 在消息平台集成上更成熟，OpenClaw 更轻量。

---

### 3. MCP 支持

**OpenClaw：** 原生支持 MCP (Model Context Protocol)
- `openclaw-mcp` 系列工具完善
- 可以连接各种 MCP 服务器

**Hermes：** 也有 MCP 工具支持
- 内置 `mcp` toolset
- 可配置 MCP 服务器

**对比：** 两者都有 MCP 支持，OpenClaw 的 MCP 生态更丰富。

---

### 4. CLI 体验

**OpenClaw：**
```bash
clawhub install xxx      # 安装技能
clawhub explore          # 浏览技能
clawhub inspect <slug>   # 查看技能详情
```
界面现代化，文档清晰。

**Hermes：**
```bash
hermes               # 交互式 CLI
hermes skills        # 管理技能
hermes tools         # 管理工具
```
功能丰富，但复杂度更高。

---

### 5. 部署方式

**OpenClaw：** 纯本地 CLI
- 下载即用
- 无需服务器

**Hermes：** 支持多种模式
- 本地 CLI
- Gateway 服务（可后台运行）
- 支持定时任务（Cron）
- 远程消息接入

---

## 三、各自优缺点

### OpenClaw 优缺点

**✅ 优点：**
- 技能生态完善，ClawHub 社区活跃
- 安装体验极佳（一句命令）
- 版本化管理，支持 rollback
- 创始人有成熟产品背景，质量有保证
- 开源透明

**❌ 缺点：**
- 主要面向海外用户，中文资料少
- 需要自己部署消息平台
- 无内置 gateway

---

### Hermes 优缺点

**✅ 优点：**
- 消息平台集成完善（飞书、QQ 等国内平台）
- 支持远程 gateway
- 内置定时任务
- 本地优先，数据在自己手上
- 支持多消息平台同时接入

**❌ 缺点：**
- Skill 生态不如 OpenClaw 成熟
- 安装新 Skill 需要手动导入
- 文档偏向开发者
- 配置相对复杂

---

## 四、我的选择建议

| 场景 | 推荐 |
|------|------|
| 纯 CLI 使用，追求技能生态 | **OpenClaw** |
| 需要接飞书/Telegram/QQ | **Hermes** |
| 想建自己的 AI 对话服务 | **Hermes** |
| 快速安装分享 Skill | **OpenClaw** |
| 国内用户，不想折腾 | **Hermes** |

---

## 五、写在最后

两个平台其实不冲突。OpenClaw 适合作为技能中心，Hermes 适合作为日常使用的 Agent。我现在把 OpenClaw 的技能导入到 Hermes 里用，两者结合效果不错。

如果你对某个平台感兴趣，可以去他们的 GitHub 看看源码，链接在上面。

---

*这篇文章全程在飞书里口述，由辉仆整理发布。博客地址：[godsay1983.github.io](https://godsay1983.github.io)*

> 🔥 *这就是 AI Agent 的魅力——工具在进化，我们也在进化。*
