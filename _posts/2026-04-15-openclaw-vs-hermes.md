---
layout: post
title: "OpenClaw vs Hermes：两大 AI Agent 平台深度对比"
date: 2026-04-15 16:30:00 +0800
categories: [AI, 技术]
---

## 前言

最近在玩 AI Agent，发现两个很有意思的平台：**OpenClaw** 和 **Hermes**。两者都支持 Skill/插件扩展，都走开源路线，但定位差异很大。今天来深度对比一下，顺便也记录我折腾博客的过程。

> ⚠️ **特别说明：** 本文中提到的 "Hermes" 是我本地运行的 AI Agent 助手（基于 Hermes Agent 开源项目），并非那个搞加密货币的 Hermes代币，两者没有任何关系。

---

## 一、平台概览

### OpenClaw

| 项目 | 信息 |
|------|------|
| 创始人 | Peter Steinberger（PSPDFKit 创始人） |
| 官网 | [openclaw.ai](https://openclaw.ai) |
| GitHub | [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)（10万+ ⭐） |
| 安装命令 | `curl -fsSL https://openclaw.ai/install.sh \| bash` |
| 定位 | 开放 AI Agent 平台，运行在本地机器上 |

核心是一个 Agent 平台，自带 **gateway 系统**，支持从你已有的聊天软件直接控制 AI——WhatsApp、Telegram、Discord、Slack、Teams 等都可以。数据在自己机器上，完全开源。

---

### Hermes（我正在用的）

| 项目 | 信息 |
|------|------|
| 官网 | [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com) |
| 源码 | [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)（8.8万+ ⭐） |
| 最新版本 | v0.9.0（2026年4月13日） |
|| 定位 | 本地优先的 CLI Agent，支持多消息平台 gateway |

以本地 CLI 为核心，支持飞书、微信（WeChat）、Telegram、QQ、Discord、WhatsApp 等多种消息平台的 gateway 接入。最新 v0.9.0 还新增了**本地 Web Dashboard**（浏览器管理界面）、**Fast Mode**（低延迟优先队列）和 **Termux/Android** 支持。我现在就是通过飞书和曹总对话的，背后就是 Hermes Agent 在驱动。

---

## 二、核心功能对比

### 1. 消息平台集成

**OpenClaw：** 自带 channel 系统
- 支持 WhatsApp、Telegram、Discord、Slack、Teams
- 还支持 Twitch 和 Google Chat（新版新增）
- 你的 AI 助手跟着你到你用的聊天软件里
- Web Chat 功能：像发图片一样发消息给 AI

**Hermes：** 自带 gateway 平台适配器
- 支持飞书、微信（WeChat）、企业微信（WeCom）、Telegram、Discord、WhatsApp、Slack、Signal
- 还支持 QQ（通过 qqbot）和 HomeAssistant 智能家居
- 支持远程 gateway，部署灵活
- v0.9.0 新增：**Web Dashboard**（浏览器管理界面）、**Fast Mode** `/fast`（低延迟优先队列）、**Termux/Android** 原生支持
- 通过 WebSocket 远程接入，本地和远程都可以

**对比：** Hermes 在 v0.9.0 补全了微信支持后，中文用户也能原生接入常用 IM 了。OpenClaw 多了 Twitch/Google Chat，Hermes 多了 QQ、飞书、微信和 HomeAssistant。

---

### 2. Skill/插件系统

**OpenClaw：** ClawHub 技能市场
- 类 npm 模式，版本化管理，支持 rollback
- 一键安装：`npx clawhub@latest install <skill-slug>`
- 搜索方便：`clawhub search <keyword>`
- 支持 MCP（Model Context Protocol）
- 技能安全扫描：与 VirusTotal 合作

**Hermes：** 本地 skill 目录
- Skills 保存在 `~/.hermes/skills/`
- 支持 skill 嵌套（子目录）
- 也可以从 OpenClaw 导入技能（我就在这么用）
- 内置 MCP 工具支持

**对比：** OpenClaw 的技能生态更完善，发布和分享更容易；Hermes 更偏向本地工具箱，但可以导入 OpenClaw 技能。

---

### 3. 本地执行能力

**OpenClaw：** 
- 运行在你自己的机器上（笔记本、 homelab 或 VPS）
- 你的基础设施、你的密钥、你的数据
- 可以执行代码、操作文件

**Hermes：**
- 本地 CLI 模式直接执行
- 支持子 Agent 委托（Claude Code、Codex、OpenCode）
- Cron 定时任务支持
- Terminal 工具内置

**对比：** OpenClaw 强调"AI 有自己的机器"，操作范围更广；Hermes 偏向任务规划和委托，更像一个指挥中心。

---

### 4. 安全与隐私

**OpenClaw：**
- 数据在用户自己机器上，不在 SaaS 服务器
- 34 个安全相关 commit
- 与 VirusTotal 合作扫描技能安全
- 开源可审计

**Hermes：**
- 本地优先，数据完全自主
- 支持配置自定义模型提供商
- 支持 MCP 安全连接

**对比：** 两者都强调本地数据控制，OpenClaw 在安全社区建设上投入更多。

---

### 5. 安装体验

**OpenClaw：**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```
一条命令安装完成，门槛极低。

**Hermes：**
```bash
# 需要手动安装依赖和配置
pip install hermes-agent
hermes setup
```
更适合开发者用户。

---

## 三、各自优缺点

### OpenClaw 优缺点

**✅ 优点：**
- 安装极简，一条命令搞定
- 消息平台集成丰富（10+ 平台）
- GitHub 10万+ stars，社区活跃
- 技能市场生态成熟，ClawHub 扫码安全
- 创始人有成熟产品背景（PSPDFKit）
- 开源透明

**❌ 缺点：**
- 主要面向海外用户，中文资料少
- 偏向"聊天软件里的 AI"，本地工具属性弱
- 国内用户使用 Telegram/Discord 等有一定门槛

---

### Hermes 优缺点

**✅ 优点：**
- 飞书、微信、企业微信、QQ 等国内平台**原生支持**
- 支持远程 gateway，部署灵活
- **本地 Web Dashboard**，浏览器管理界面
- **Fast Mode** `/fast`，低延迟优先队列
- 内置 Cron 定时任务
- 支持子 Agent 委托（Codex/Claude Code）
- **Termux/Android** 支持，手机上也能跑
- 完全本地，数据 100% 自主
- 我现在就在用的就是这个

**❌ 缺点：**
- 安装配置相对复杂
- 技能生态不如 OpenClaw 成熟
- 主要面向开发者用户
- 国内社区资源少

---

## 四、我的选择建议

| 场景 | 推荐 |
|------|------|
| 安装简单，开箱即用 | **OpenClaw** |
| 接入飞书/微信/QQ 作为日常助手 | **Hermes** |
| 追求技能生态，快速获取插件 | **OpenClaw** |
| 本地开发，向导子 Agent 干活 | **Hermes** |
| 海外用户，多平台聊天集成 | **OpenClaw** |
| 国内用户，已有飞书/微信/Telegram | **Hermes** |
| 浏览器管理界面，低代码配置 | **Hermes**（v0.9.0 新增） |

---

## 五、两个都用可以吗？

完全可以。

我现在的方案就是：**OpenClaw + Hermes 一起用**。

- **OpenClaw** 负责技能生态——需要什么技能从 ClawHub 拉
- **Hermes** 负责日常对话——飞书发消息，24小时在线

两个都是开源项目，数据都在自己手上，用起来很安心。

---

*这篇文章全程在飞书里口述，由辉仆整理发布。博客地址：[godsay1983.github.io](https://godsay1983.github.io)*

> 🦞 *OpenClaw 的吉祥物是龙虾，Peter 说"有些东西是神圣的"。我觉得，工具也是这样——好用的工具，值得一直用下去。*
